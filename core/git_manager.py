import subprocess


def git_commit(message):

    try:

        subprocess.run(["git", "add", "."], check=True)

        subprocess.run(
            ["git", "commit", "-m", message],
            check=False
        )

        subprocess.run(
            ["git", "push"],
            check=False
        )

        print("Git commit realizado")

    except Exception as e:

        print("Error en git:", e)
