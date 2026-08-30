import os

import gh_cli

IS_MERGED = os.environ.get("IS_MERGED", "false")

MSG_MERGED = """
{},

Congratulations on your first merged contribution! 🎉✨
Thank you for joining the community — your PR is now a part of the Plugin Catalogue!

A few friendly reminders:
🕒 Your changes may take a short time to appear in the catalogue.
✅ Check back later to make sure everything displays as expected.

We’re thrilled to welcome you as a contributor and hope to see more from you in the future!
Welcome aboard, and happy coding! 🚀
""".strip()

FIRST_TIME_HEADER = """
**Hi, {}!**  
This is your first contribution to the xiepy. Welcome! 🎉  

We’ll review your PR soon — thanks for your patience!
Hope you have a great day!
""".strip()

MSG_HEADER = """
Thanks for your contribution! 🎉
Please be patient before we done checking.
Have a nice day!
""".strip()


def hello(author, is_first_time):
    if is_first_time:
        msg = FIRST_TIME_HEADER.format(f"@{author}")
    else:
        msg = MSG_HEADER
    gh_cli.pr_comment(msg)


def main():
    author, is_first_time = gh_cli.check_contributor()
    if not author:
        author = "Contributor"

    hello(author, is_first_time)


if __name__ == "__main__":
    main()
