import traceback
import os

features = {}
features_id = {}
features_description = {}


def register_feature(description="暂无描述"):
    def wrap(func):
        if func.__name__ not in features.keys():
            feature_name = func.__name__
            features[feature_name] = func
            features_description[feature_name] = description
        return func

    return wrap


def run_feature(func):
    print(f"运行功能：{func.__name__}")
    return func()


def show_description():
    for n, (k, v) in enumerate(features.items()):
        features_id[n] = k
        print(f'{n}: {k}')
        print(features_description[k])


@register_feature(description="""用于显示所有的功能
""")
def show_features():
    print('目前以下功能可用：')
    for n, (k, v) in enumerate(features.items()):
        features_id[n] = k
        print(f'{n}: {k}', end=' ')
        print(f"({features_description[k].splitlines()[0]})")


class StringBuffer:
    def __init__(self):
        self.s = ''

    def prints(self, s, end='\n'):
        print(s, end=end)
        self.s = self.s + s + end


@register_feature()
def read_dump(tofile=False):
    sb = StringBuffer()
    path = input('input dump path: ').strip('\"') or "example.dump"
    with open(path, 'rb') as fp:
        x = fp.read()
    sb.prints('data: ')
    x_set = [x[i:i + 1] for i in range(len(x))]
    keys = []
    sector = 0
    for i in range(0, len(x_set), 16):
        row = x[i:i + 16]
        s = [x_.decode('ascii').replace('\n', '.') if x_.isascii() and x_ > b'\x20' and x_ != b'\x7f'
             else "." for x_ in x_set[i:i + 16]]
        sb.prints(f"sector {sector:02}: {''.join(row.hex())} {''.join(s)}")
        # print(i)
        if ((i / 16) + 1) % 4 == 0:
            key = row[:6]
            sector += 1
            keys.append(key.hex())
            sb.prints('')
    sb.prints('keys: ')
    for k in set(keys):
        sb.prints(k)
    if tofile:
        npath, ext = os.path.splitext(path)
        with open(npath + '.txt', 'w') as fp:
            fp.write(sb.s)


@register_feature()
def dump_txt():
    read_dump(tofile=True)


if __name__ == '__main__':
    try:
        show_features()
        opt = input("请输入要运行的功能编号（输入help查看完整功能描述）：")
        if opt == "help":
            show_description()
        elif opt.isalnum() and int(opt) < len(features):
            run_feature(features[features_id[int(opt)]])
        else:
            print("无法识别此功能。")
    except Exception as err:
        print(err)
        traceback.print_exc()
