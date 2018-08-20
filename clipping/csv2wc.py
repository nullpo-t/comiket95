__author__ = 'ebiiim'
__copyright__ = 'Copyright 2018, ぬるぽ帝国'
__license__ = 'MIT'

from datetime import datetime, timedelta, timezone
import random
import csv
from wordcloud import WordCloud


def conv_csv_wctext(csv_path):
    s = ''
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s += (row['word'] + ' ') * int(row['frequency'])
    return s


def randomize(text):
    l = text.split(' ')
    return ' '.join(random.sample(l, len(l)))


def generate_wordcloud(text, font_path=None):
    return WordCloud(background_color='white', width=590, height=700,
                     font_path=font_path, max_font_size=128,
                     regexp=r"\w[\w'|()._-]+"  # include symbols
                     ).generate(text)


def mono_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % 0  # monochrome


def add_timestamp(filepath):
    now = datetime.now(timezone(timedelta(), 'UTC'))
    tmp = filepath.split('.')
    return "{0}_{1:%Y%m%dT%H%M%SZ}.{2}".format('.'.join(tmp[:-1]), now, tmp[-1])


if __name__ == '__main__':
    font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'  # macOS
    csv_path = './wordlist.csv'
    color_output_path = add_timestamp('./output/clipping_color.png')
    mono_output_path = add_timestamp('./output/clipping_mono.png')

    text = randomize(conv_csv_wctext(csv_path))
    wc = generate_wordcloud(text, font_path)
    wc.to_file(color_output_path)
    wc = wc.recolor(color_func=mono_color_func)
    wc.to_file(mono_output_path)
