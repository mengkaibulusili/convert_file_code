import click
import os
import chardet
import re

default_path = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option(
    "--source_dir",
    default=default_path,
    prompt="source of dir. default: ",
)
@click.option(
    "--target_encoding",
    default="utf-8",
    prompt="target_encoding: [utf-8/gbk/..]. default: ",
)
@click.option(
    "--match",
    default=".*\.(txt|py)$",
    prompt="match: x.txt or x.py default: ",
)
def convert(**kwargs):
    default_encoding = "utf-8"
    print("match %s" % kwargs.get("match"))
    _pattern = re.compile(kwargs.get("match"))

    def convert_single_file(abs_path):
        s = b""
        with open(abs_path, mode="rb+") as f:
            s = f.read()
        source_encoding = chardet.detect(s).get("encoding")
        print(f"file {abs_path} code :{source_encoding} --> {default_encoding}")

        with open(abs_path, encoding=default_encoding, mode="w") as f:
            f.write(s.decode(source_encoding))

    default_encoding = kwargs.get("target_encoding")
    for root, _, files in os.walk(kwargs.get("source_dir")):

        def _match(f_name):
            print(f_name, bool(re.match(_pattern, f_name)))
            return bool(re.match(_pattern, f_name))

        def _f(f_name):
            abs_path = os.path.join(root, f_name)
            convert_single_file(abs_path)

        list(map(_f, filter(_match, files)))


if __name__ == "__main__":
    convert()
