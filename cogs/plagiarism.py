import requests
import json
import os
import sys

from discord.ext import commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db


def plagiarism(text: str) -> dict:
    plag_checker_url = "https://papersowl.com:443/plagiarism-checker-send-data"
    cookies = {
        "PHPSESSID": "qjc72e3vvacbtn4jd1af1k5qn1",
        "first_interaction_user": "%7B%22referrer%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com%5C%2F%22%2C%22intern"
        + "al_url%22%3A%22%5C%2Ffree-plagiarism-checker%22%2C%22utm_source%22%3Anull%2C%22utm_medium%22%3Anull%2C%2"
        + "2utm_campaign%22%3Anull%2C%22utm_content%22%3Anull%2C%22utm_term%22%3Anull%2C%22gclid%22%3Anull%2C%22msc"
        + "lkid%22%3Anull%2C%22adgroupid%22%3Anull%2C%22targetid%22%3Anull%2C%22appsflyer_id%22%3Anull%2C%22appsfly"
        + "er_cuid%22%3Anull%2C%22cta_btn%22%3Anull%7D",
        "first_interaction_order": "%7B%22referrer%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com%5C%2F%22%2C%22inter"
        + "nal_url%22%3A%22%5C%2Ffree-plagiarism-checker%22%2C%22utm_source%22%3Anull%2C%22utm_medium%22%3Anull%2C%"
        + "22utm_campaign%22%3Anull%2C%22utm_content%22%3Anull%2C%22utm_term%22%3Anull%2C%22gclid%22%3Anull%2C%22ms"
        + "clkid%22%3Anull%2C%22adgroupid%22%3Anull%2C%22targetid%22%3Anull%2C%22appsflyer_id%22%3Anull%2C%22appsfl"
        + "yer_cuid%22%3Anull%2C%22cta_btn%22%3Anull%7D",
        "affiliate_user": "a%3A3%3A%7Bs%3A9%3A%22affiliate%22%3Bs%3A9%3A%22papersowl%22%3Bs%3A6%3A%22medium%22%3B"
        + "s%3A9%3A%22papersowl%22%3Bs%3A8%3A%22campaign%22%3Bs%3A9%3A%22papersowl%22%3B%7D",
        "sbjs_migrations": "1418474375998%3D1",
        "sbjs_current_add": "fd%3D2022-05-24%2019%3A01%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fpapersowl.com%2Ffree-plagi"
        + "arism-checker%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
        "sbjs_first_add": "fd%3D2022-05-24%2019%3A01%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fpapersowl.com%2Ffree-plagiar"
        + "ism-checker%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
        "sbjs_current": "typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%"
        + "7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
        "sbjs_first": "typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7C"
        + "cnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
        "sbjs_udata": "vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%206.3%3B%20"
        + "Win64%3B%20x64%3B%20rv%3A100.0%29%20Gecko%2F20100101%20Firefox%2F100.0",
        "sbjs_session": "pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fpapersowl.com%2Ffree-plagiarism-checker",
        "_ga_788D7MTZB4": "GS1.1.1653411683.1.0.1653411683.0",
        "_ga": "GA1.1.1828699233.1653411683",
        "trustedsite_visit": "1",
        "trustedsite_tm_float_seen": "1",
        "AppleBannercookie_hide_header_banner": "1",
        "COOKIE_PLAGIARISM_CHECKER_TERMS": "1",
        "plagiarism_checker_progress_state": "1",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:100.0)Gecko/20100101 Firefox/100.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://papersowl.com/free-plagiarism-checker",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://papersowl.com",
        "Dnt": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Te": "trailers",
        "Connection": "close",
    }
    request_data = {
        "is_free": "false",
        "plagchecker_locale": "en",
        "product_paper_type": "1",
        "title": "",
        "text": text,
    }

    res = requests.post(
        plag_checker_url, headers=headers, cookies=cookies, data=request_data
    )
    return json.loads(res.text)


class Plagiarism(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Instructor")
    @commands.command(
        name="check_plagiarism", help="check attached txt file for plagiarism"
    )
    async def check_plagiarism(self, ctx):
        if len(ctx.message.attachments) != 1:
            await ctx.send("Must have exactly one attachment")
            return

        attachment_url = ctx.message.attachments[0].url
        response = requests.get(attachment_url, timeout=10)

        res = plagiarism(response.text)

        await ctx.author.send(
            f'Word count: {res["words_count"]}\n'
            + f'Percent plagiarism: {str(100 - float(res["percent"]))}\n'
            + f'Matches: {str(res["matches"])}'
        )

    @commands.has_role("Instructor")
    @commands.command(name="grade_for_plagiarism", help="")
    async def grade_for_plagiarism(
        self, ctx, member_name: str, assignment_name: str, max_plagiarism_percent: str
    ):
        max_plagiarism_percent = float(max_plagiarism_percent)

        if len(ctx.message.attachments) != 1:
            await ctx.send("Must have exactly one attachment")
            return

        if max_plagiarism_percent > 1:
            await ctx.send(
                "max_plagiarism_percent is a decimal. Ex: 0.5 represents 50%"
            )
            return

        attachment_url = ctx.message.attachments[0].url
        response = requests.get(attachment_url, timeout=10)

        res = plagiarism(response.text)

        if (100 - float(res["percent"])) >= (
            max_plagiarism_percent * 100
        ):  # greater-than or equal to % plagiarized
            grade_exists = (
                db.query(
                    """SELECT COUNT(grade)
                FROM grades
                JOIN assignments ON id = assignment_id
                WHERE assignment_name = %s""",
                    (assignment_name,),
                )[0][0]
                > 0
            )

            if grade_exists:
                # Plagiarized, set exisiting grade to zero
                db.query(
                    """UPDATE grades
                    SET grade = 0
                    FROM assignments
                    WHERE member_name = %s AND assignment_id = id AND assignment_name = %s""",
                    (member_name, assignment_name),
                )
                await ctx.author.send("Assignment was plagiarized, grade set to zero")
            else:
                # Plagiarized, input new grade as zero
                db.query(
                    """INSERT INTO grades
                    SELECT name_mapping.guild_id, %s AS member_name, id, 0 AS some_column
                    FROM name_mapping
                    JOIN assignments ON username = %s AND assignment_name = %s""",
                    (member_name, member_name, assignment_name),
                )
                await ctx.author.send(
                    "Assignment was plagiarized, grade newly inputted to zero"
                )

        else:
            # No plagiarized
            await ctx.author.send(
                "Assignment not was plagiarized. If a grade exists, it was unchanged"
            )


async def setup(bot):
    """Adds the file to the bot's cog system"""
    await bot.add_cog(Plagiarism(bot))
