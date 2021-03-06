#!/usr/bin/python2.7
# -*-coding:UTF-8 -*

import redis
import argparse
import ConfigParser
from pubsublogger import publisher

import matplotlib.pyplot as plt


def main():
    """Main Function"""

    # CONFIG #
    cfg = ConfigParser.ConfigParser()
    cfg.read('./packages/config.cfg')

    # SCRIPT PARSER #
    parser = argparse.ArgumentParser(
        description='''This script is a part of the Analysis Information Leak framework.''',
        epilog='''''')

    parser.add_argument('-f', type=str, metavar="filename", default="figure",
                        help='The absolute path name of the "figure.png"',
                        action='store')

    args = parser.parse_args()

    # REDIS #
    r_serv = redis.StrictRedis(
        host=cfg.get("Redis_Level_DB_Hashs", "host"),
        port=cfg.getint("Redis_Level_DB_Hashs", "port"),
        db=cfg.getint("Redis_Level_DB_Hashs", "db"))

    # LOGGING #
    publisher.port = 6380
    publisher.channel = "Graph"

    # FUNCTIONS #
    publisher.info("""Creating the Repartition Graph""")

    total_list = []
    codepad_list = []
    pastie_list = []
    pastebin_list = []
    for hash in r_serv.keys():
        total_list.append(r_serv.scard(hash))

        code = 0
        pastie = 0
        pastebin = 0
        for paste in r_serv.smembers(hash):
            source = paste.split("/")[5]

            if source == "codepad.org":
                code = code + 1
            elif source == "pastie.org":
                pastie = pastie + 1
            elif source == "pastebin.com":
                pastebin = pastebin + 1

        codepad_list.append(code)
        pastie_list.append(pastie)
        pastebin_list.append(pastebin)

    codepad_list.sort(reverse=True)
    pastie_list.sort(reverse=True)
    pastebin_list.sort(reverse=True)

    total_list.sort(reverse=True)

    plt.plot(codepad_list, 'b', label='Codepad.org')
    plt.plot(pastebin_list, 'g', label='Pastebin.org')
    plt.plot(pastie_list, 'y', label='Pastie.org')
    plt.plot(total_list, 'r', label='Total')

    plt.xscale('log')
    plt.xlabel('Hashs')
    plt.ylabel('Occur[Hash]')
    plt.title('Repartition')
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.savefig(args.f+".png", dpi=None, facecolor='w', edgecolor='b',
                orientation='portrait', papertype=None, format="png",
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=True)

if __name__ == "__main__":
    main()
