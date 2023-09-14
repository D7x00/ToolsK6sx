from datetime import datetime
from Encrypt import CustomEncryption
from lib.Color import *
import os
import argparse
from time import sleep

RunAllTools: bool = False
TextEnc: bool = False
TextSave: bool = False


def Run() -> None:
    while (True):
        os.system("clear")
        # Show banner
        print(Color.banner + Color.ShowBanner() + Color.Reset)

        # input Num
        print(Color.Green)
        k6sx = input(f"{Color.ANSI_BOLD}$ >> {Color.ANSI_RESET}")
        print(Color.Reset)

        # logic
        if k6sx == "1":
            CustomEncryption.main()

        elif k6sx == "exit":
            exit(0)

def main():

    parser = argparse.ArgumentParser(

        prog=f"{Color.ANSI_BOLD}{Color.Blue}Tools6sx{Color.Reset}{Color.Reset}",
        usage=f"{Color.ANSI_BOLD}{Color.Blue}Explain Using{Color.Reset}{Color.Reset}",
        add_help=True
    )
    Group = parser.add_argument_group(f"{Color.banner}For Encryption :{Color.Reset}")
    parser.add_argument(
        "--m",
        f"--run",
        help=f"{Color.ANSI_GREEN }--m or --run For Run  AllTools{Color.ANSI_1RESET}",
        action='store_const',
        const=True,
        default=False,
        dest="RunAllTools"
    )
    Group.add_argument(
        "--tf",
        "--text--file",
        help=f"{Color.ANSI_YELLOW}--tf or --text--file For Encryption text and save text and salat in file.{Color.ANSI_1RESET}",
        action='store_const',
        const=True,
        default=False,
        dest="TextSave"
    )
    Group.add_argument(
        "--t",
        "--text",
        help=f"{Color.ANSI_YELLOW}--t or --text For Encryption text only and return text Encryption and salat.{Color.ANSI_1RESET}",
        action='store_const',
        const=True,
        default=False,
        dest="TextEnc"
    )

    args = parser.parse_args()

    if args.RunAllTools:
        Run()
    elif args.TextEnc:
        if args.TextSave:
            print("Encrypt Text And Save ")

        else:
            print("Encrypt Text Not Save ")


if __name__ == "__main__":

    print(f"\n{Color.ANSI_BOLD}{Color.banner}Starting Tools6sx ..........  {datetime.now().time()}{Color.Reset}{Color.ANSI_RESET}\n")
    sleep(1)
    main()