# DATASCI 350 - Data Science Computing

## Quiz 03 - Local LLMs and cloud computing

You will build a local chatbot with Ollama, call it from Python, and run an analysis on an AWS EC2 instance.

This quiz is worth 6% of the final grade, and covers lectures 12, 14, 15, 16 and 17. It is open-book and open-notes. It is an individual assessment, so please do not discuss the questions with your colleagues during class. You have 75 minutes.

You may use AI tools, but you must be able to explain every command and line you submit. I may ask any student to walk me through part of their work during or after the quiz.

At the end of `commands.txt`, say which tasks used AI and which tool, give one example prompt, and say if an AI agent ran commands for you. Any task you do not list counts as done without AI. If you used none, write `AI: none`.

Answers you cannot explain, and AI use you do not list, earn no points.

### Rules

- Fork and clone this repository.
- Record every command, explanation and requested output in `commands.txt`, in the repository root on your laptop. Write git commands there before you run them.
- Paste text. Screenshots are not accepted.
- Work in the command line and your editor. You may fork on the GitHub website, but files created or uploaded there lose points.
- Use the AWS console only to launch the instance, find its public DNS and, at the end of the quiz, terminate it.
- When you finish, post your fork's link on Canvas, under "Assignments", Quiz 03.

## Activity 1: A sports-commentator chatbot with Ollama

Lecture 12 covers everything in this activity.

1. Download `granite4:350m`. Paste the output of `ollama show` and `ollama ls` for it into `commands.txt`. Use the [rule from lecture 12](https://danilofreire.github.io/datasci350/lectures/lecture-12/12-local-models.html#/quantisation) to predict its size on disk from its parameters and quantisation, then write your prediction next to the size that `ollama ls` reports. (`BF16` uses 16 bits per weight.)

2. Create `ollama/Modelfile` with `FROM granite4:350m`, `temperature` plus one other `PARAMETER`, and a `SYSTEM` block. The persona is an over-excited live sports commentator. State three rules: answers are at most four sentences, the model always addresses the user as "sports fans", and it says so on air when it does not know something.

3. Build the model with `ollama create`, naming it `commentator`. Add one sentence explaining why this command downloads nothing.

4. Run these two prompts, each as a separate `ollama run` command. Paste each response and note which rules held, which broke and which did not apply:

    - `"What does git commit do?"`
    - `"What is the weather in Atlanta right now?"`

5. Add a `MESSAGE` example to your `Modelfile` that teaches the model to say it does not know the weather, then rebuild it. Run the weather prompt three times, paste the responses, and say how many times the model admitted it did not know. Hint: see the ["Teaching by example" slide](https://danilofreire.github.io/datasci350/lectures/lecture-12/12-local-models.html#/teaching-by-example) in lecture 12.

6. Stage the `ollama/` folder and `commands.txt`, commit with the message "Add commentator chatbot", and push.

## Activity 2: Calling the model from Python

Lecture 14 covers this activity. Your `MESSAGE` example may make the model give odd answers or refuse questions. That is fine, because these tasks are about the script output.

7. Run `ollama/ask_local.py`, which asks `granite4:350m` a question and prints `response.usage`. In the script, change the model to `commentator` and run it again. Paste both outputs into `commands.txt`. In one sentence, why does `commentator` use more `prompt_tokens` for the same question?

8. Run `ollama/ask_json.py`. It fails. Paste the error and the `finish_reason` it prints into `commands.txt`. Change one line so the script works, then paste the new output. In one sentence, why did the script fail? Stage `ollama/` and `commands.txt`, commit with the message "Add Python calls", and push.

## Activity 3: Data analysis on AWS EC2

Lectures 16 and 17 cover this activity. The `aws/` directory holds `traffic_analysis.py` and `website_traffic.txt`: 30 days of fictional website traffic. The script prints summary statistics and saves a plot as `traffic_analysis.png`.

9. Launch an EC2 instance from the AWS console: Ubuntu Server 26.04 LTS, instance type `t3.micro`, with a name of your choice and a security group that allows SSH. In the same launch wizard, create a new ED25519 key pair as a `.pem` file, or reuse one you already have. Never commit the `.pem` file: this repository's `.gitignore` already excludes `*.pem`.

10. Set the key's permissions with `chmod 400`, then connect to the instance with `ssh -i`. Copy the remote shell prompt line into `commands.txt` as proof that you are on the instance.

11. On the instance, update the package lists, then install `python3-pandas`, `python3-matplotlib` and `python3-seaborn` with apt. Add the commands to `commands.txt`.

12. In a new terminal on your laptop, copy `aws/traffic_analysis.py` and `aws/website_traffic.txt` to the instance with `scp`. Run `scp` from the repository root, with the full path to your key.

13. On the instance, run `traffic_analysis.py` with `python3` and redirect its output into a file named `results.txt`. Then, still on the instance, paste these two commands exactly as written. The first adds your instance's ID to `results.txt`, and the second saves a hash of that file in `fingerprint.txt`:

    ```bash
    cat /var/lib/cloud/data/instance-id >> results.txt
    sha256sum results.txt > fingerprint.txt
    ```

14. In the terminal on your laptop, from the repository root, copy `results.txt`, `fingerprint.txt` and `traffic_analysis.png` back from the EC2 instance into the `aws/` folder with `scp`, using the full path to your key.

15. Answer in `commands.txt`, in one sentence: when you STOP an instance rather than terminate it, what do you still pay for? Then terminate the instance, add your AI note, **stage everything**, commit with the message "Add AWS analysis results", and push. Done! 😊

### Bonus task

Attempt this only after finishing the main tasks, if you still have time. Document every step in `commands.txt`, then commit and push again.

The `rag/` folder holds `rag.py` and its corpus from lecture 15. The script needs `ollama pull embeddinggemma`, the `llama3.2:1b` model and `pip install ollama chromadb`, as in the lecture exercise. From inside `rag/`, run `python rag.py` twice and type a question each time: first "How big is the llama3.2:1b download?", then "Who won the 2022 World Cup?". Paste both outputs into `commands.txt`, with one sentence on why retrieval still returns three chunks for the World Cup question, and what the similarities tell you.

Best of luck!
