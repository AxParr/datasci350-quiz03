# DATASCI 350 - Data Science Computing

## Quiz 03 - AI-assisted programming and cloud computing

### The scenario

You will do three things in this quiz. First, you will build a local chatbot with Ollama and give it a personality with a `Modelfile`. Second, you will call that model from Python and handle an API key safely. Third, you will rent a Linux machine on AWS EC2, send a small analysis script to it, run it there, and bring the results back.

This quiz is worth 6% of the final grade, and covers lectures 12, 14, 15, 16 and 17. It is open-book and open-notes. It is an individual assessment: please do not discuss the questions with your colleagues during class. You have 75 minutes.

You may use AI tools on the same terms as the rest of the course: they are allowed, and you must be able to explain every command and every line you submit. The instructor may ask any student to walk through part of their work, during the quiz or right after it. An answer you cannot explain earns no marks.

### Rules

- Record every command you run in a file named `commands.txt` in the repository's root directory. Where a task asks for a short explanation or for pasted output, write it in `commands.txt` too.
- Work from the command line and your editor throughout. Files created or uploaded through the GitHub website lose points: the grader reads your commit history.
- **Screenshots are not accepted.** Model responses, terminal output and prompts go in as copy-pasted text.
- There is one exception to the command-line rule. Launching the EC2 instance happens in the AWS console because there is no other way to do it. Everything after you connect to the instance is terminal work.
- When you finish, post the link to your fork on Canvas, in the "Assignments" tab under Quiz 03.

### If `git push` asks for credentials

Your machine should already be logged in to GitHub. If a push fails with an authentication error, do not waste time creating tokens: run `gh auth login`, choose GitHub.com, then HTTPS, and log in with the browser. After that, `git push` works normally.

### Setup

1. Fork this repository to your GitHub account.
2. Clone your fork to your machine with the command line.
3. Change directory into the cloned repository.
4. Create `commands.txt` in the root of the repository.

## Activity 1: A sports-commentator chatbot with Ollama

Lecture 12 covers everything in this activity.

1. Pull one small model: `llama3.2:1b` or `gemma3:1b`. Both are around 1 GB and run comfortably on a laptop. Then run `ollama ls` and paste the output into `commands.txt`.

2. Run `ollama show` on the model you pulled. Record its parameter count, context length and quantization in `commands.txt`. Add one sentence explaining how the quantization links the parameter count to the size on disk that `ollama ls` reports.

3. Create a directory named `ollama` in the repository, and a file named `Modelfile` inside it. The `Modelfile` must contain a `FROM` line, at least two `PARAMETER` lines (`temperature` plus one other of your choice), and a `SYSTEM` block. The `SYSTEM` block gives the model its persona: an over-excited live sports commentator who narrates every answer like a play-by-play broadcast. State these three rules in the prompt:

    1. Answers are at most four sentences long.
    2. The model always addresses the user as "sports fans".
    3. If the model does not know something, it says so on air instead of inventing an answer.

4. Build the model with `ollama create`, naming it `commentator`. Add one sentence to `commands.txt` explaining why this command downloads nothing from the internet.

5. Test the model with exactly these three prompts, each as a separate `ollama run` command, and paste each response into `commands.txt`:

    - `"What does git commit do?"`
    - `"What is the weather in Atlanta right now?"`
    - `"What did I ask you in yesterday's session?"`

    For each response, note which of your three rules held and which broke. Small models break rules often, and spotting the break is the point of the task.

6. Stage the `ollama/` folder and `commands.txt`, commit with the message "Add commentator chatbot", and push.

## Activity 2: Keys and calls

Lectures 14 and 15 cover this activity.

7. Write `ollama/ask_local.py`: a script that uses the `openai` package to talk to your local Ollama server, asks your model one question at temperature 0, and prints the reply. The lecture 14 slides show how to point the client at the local server. Run the script twice and note in `commands.txt` whether the two outputs match, with one sentence on why.

8. Create a `.env` file in the repository root with a fake key line, for example `OPENROUTER_API_KEY=not-a-real-key`. Add `.env` to `.gitignore`, then run `git status` and paste the output into `commands.txt` to show that git no longer sees the file. Add one sentence to `commands.txt`: if a real key had already been committed and pushed, why is deleting the commit not enough?

9. Short answer in `commands.txt`, two or three sentences. A RAG system gives a wrong answer. How would you tell whether retrieval or generation failed? Lecture 15 has the pipeline you need. Then stage your Activity 2 work and `commands.txt`, commit with the message "Add keys and calls", and push.

## Activity 3: Data analysis on AWS EC2

Lectures 16 and 17 cover this activity. The `aws/` directory holds `traffic_analysis.py` and `website_traffic.txt`: 30 days of fictional website traffic. The script prints summary statistics and saves a plot as `traffic_analysis.png`.

10. Launch an EC2 instance from the AWS console: Ubuntu Server 26.04 LTS, instance type `t3.micro`, with a name of your choice and a security group that allows SSH. In the same launch wizard, create a new ED25519 key pair as a `.pem` file, or reuse one you already have. This is the one part of the quiz that happens in the browser. Never commit the `.pem` file: this repository's `.gitignore` already excludes `*.pem`.

11. Set the key's permissions with `chmod 400`, then connect to the instance with `ssh -i`. Copy the remote shell prompt line into `commands.txt` as proof that you are on the instance.

12. On the instance, update the package lists, then install `python3`, `python3-pip`, `python3-pandas`, `python3-matplotlib` and `python3-seaborn` with apt. Add the commands to `commands.txt`.

13. From your laptop, copy `aws/traffic_analysis.py` and `aws/website_traffic.txt` to the instance with `scp`.

14. On the instance, run the analysis and redirect its output into a file named `results.txt`. Then save the operating system identity with `cat /etc/os-release > os.txt`.

15. From your laptop, copy `results.txt`, `os.txt` and `traffic_analysis.png` back into the `aws/` folder of your local repository with `scp`.

16. Answer in `commands.txt`, two sentences: when you STOP an instance rather than terminate it, what do you still pay for, and what happens to its public IP address? Then terminate the instance, stage everything, commit with the message "Add AWS analysis results", and push. Done! 😊

### Bonus tasks

Attempt these only after finishing the main tasks, if you still have time. Document every step in `commands.txt`, then commit and push again.

1. Run your model with `--format json`, asking for a JSON object with the keys `answer` and `confidence`. Pipe the output through a one-line `python3 -c` command that prints only the `answer` field. Paste both the command and its output into `commands.txt`. Add `--nowordwrap` to the `ollama run` command: without it, Ollama breaks long lines and the JSON no longer parses.

2. The `rag/` folder holds `rag.py` and its corpus from lecture 15. The script needs `ollama pull embeddinggemma`, the `llama3.2:1b` model and the `ollama` Python package, as in the lecture exercise. Run it from inside `rag/` twice: once with a question the corpus can answer, and once with "What is the capital of Nepal?" (change `QUESTION` in the script). Paste both score printouts into `commands.txt`, with one sentence on why retrieval still returns chunks for the Nepal question.

Best of luck!
