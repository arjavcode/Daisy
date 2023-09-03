# Daisy
Atlan take home challenge (backend)

Following schematic diagram describes the design of the solution:
<img src="https://drive.google.com/uc?export=view&id=1QwN41d-VJB70_YrQDT4aw8wosG2P7D5Q" alt="Schematic Diagram" />

A dummy backend (`Collect Backend`) has been created to simulate Collect's form submission action. This is developed on FastAPI framework with Postgres DB. The idea was to create an ecosystem for pluggable `post-submission` tasks.

As per my understanding of the problem statement, some of these tasks can be `synchronous` (like data validation), that is, the output of the task needs to be sent along with the response on the form submission endpoint, and `asynchronous` task (like storing in google sheets) that needs to be carried out in the background.

One simple solution was to connect a task queue (like `Celery`) to the actual Collect Backend. Using this solution, the `asynchronous` task can be easily handled in different `Celery` workers but the code for it needed to be maintained in the same backend. Besides, tools like `Celery` only support asynchronous task queues. Also, **unified interface** was also a requirement. Thus, I realized that creating a separate service for handling all kinds of post-submission tasks can be a better solution.

Moving to another service adds to latency issues. For this reason, instead of REST, gRPC is preferred. gRPC uses protocol buffer message format to communicate instead of JSON and thus transfers very minimal data reducing latency. `PostSubProxy` is the gRPC server that takes request from gRPC client that is our main backend.

Now the question is when to invoke RPC methods? When post has been successfully submitted, right? For this, `decorator` design pattern is used. The function that handles the request of submitting form in main backend is decorated with `post_submission` decorator. This decorator handles connection to the gRPC server and appends the response from the gRPC server to the response. In terms of code:

```python
@app.post('/forms/{form_id}/submit')
@post_submission(rpc_stub)			# post_submission decorator
def submit(form_id: str, submission):
    pass
```

That's it! Just adding one line makes sure that the relevant tasks installed on a particular form is fired post form submission. No code overhaul on the main backend.

Now, coming to `PostSubProxy`. This contains an RPC method `Process` that gets called whenever a form is submitted (provided that form submission endpoint is registered through the decorator). This service maintains a database of `Tasks` associated with a form.  Following is the schema:

```
Task:
	id: UUID, PK
	form_id: UUID
	name: str, NOT NULL
	module: str, NOT NULL
	func: str, NOT NULL
	asyncStatus: bool, NOT NULL
```

To understand the schema, it is important to note how tasks are arranged. The tasks are treated as **apps**. Each app or a task is a separate python module located inside this server in `tasks` directory as shown below:

<img src="https://drive.google.com/uc?export=view&id=1X3b8UuPQPbgeqmC8Muabv8OFp4pvtZvh" />

In the schema, the `module` field is supposed to take the `module` name, here it is `TestTask`. The entry-point should be the file where the main entry code is located, here it is `TestTask`. Inside this, it must contain a class that should implement `TaskBase` interface. This class is instantiated and ran.

To recap the dataflow:

* User submits form to the main backend
* Main backend stores the information and returns the response.
* This response is intercepted through the `post_submission` decorator and passed to the gRPC post submission server by calling the `Process` RPC method.
* The `Process` method in the gRPC server collects meta information of all the tasks, from the database, that is supposed to be ran on this particular form.
* Runs all the synchronous tasks and then assign the asynchronous tasks to different Celery works. To communicate with the Celery workers, RabbitMQ message queue has been used.

This makes it easy to make different tasks and plug them to the form required from the gRPC server without making a single change in the backend.

Logs can be set up at both the servers on what post processing task has been initiated. Currently, the system relies on Celery logs and can restart unfinished tasks if things go south. For the synchronous tasks, a similar mechanism can be developed (not developed in this project due to time constraint).

Google Sheet has been integrated as a sample app. It uses a Service Account to connect to Google Sheets API. Since the User/Organisation module has not been implemented in the dummy backend, the sheet created is shared with a particular hardcoded email as of now but can be easily ported if we also pass the user/organisation information to the RPC method.

<hr>
