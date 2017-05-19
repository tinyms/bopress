# -*- coding: utf-8 -*-
import base64
import codecs
import decimal
import hashlib
import json
import os
import re
import tempfile
import time
import uuid
from datetime import timedelta, datetime
from random import Random

import xlrd

__author__ = 'yezang'


class DataResult(object):
    message = ""
    success = False
    data = None

    def to_dict(self):
        t = dict()
        t["message"] = self.message
        t["success"] = self.success
        t["data"] = self.data
        return t

    def to_json(self):
        return Utils.encode(self.to_dict())


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return Utils.format_datetime_short(o)

        super(JsonEncoder, self).default(o)


class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def mk_temp_file():
        return tempfile.mkstemp()[1]

    @staticmethod
    def capitalize(s):
        if not s:
            return ""
        b = s.split("_")
        c = [i.capitalize() for i in b]
        return "".join(c)

    @staticmethod
    def random_str(size=6):
        s = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(size):
            s += chars[random.randint(0, length)]
        return s

    @staticmethod
    def random_num(size=6):
        str_ = ''
        chars = '0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(size):
            str_ += chars[random.randint(0, length)]
        return str_

    @staticmethod
    def text_read(f_name, join=True):
        if not os.path.exists(f_name):
            return ""
        with codecs.open(f_name, "r", "utf-8") as f:
            all_ = f.readlines()
        if join:
            return "".join(all_)
        return all_

    @staticmethod
    def text_write(f_name, lines=list(), suffix="\n"):
        with codecs.open(f_name, "w+", "utf-8") as f:
            if isinstance(lines, list):
                for line in lines:
                    f.write(line + suffix)
            else:
                f.write(lines)
                f.write(suffix)

    @staticmethod
    def text_file_compact(f_name):
        txt = Utils.text_read(f_name, False)
        tmp_txt = list()
        for r in txt:
            m = r.strip()
            if m == "":
                continue
            tmp_txt.append(r)
        Utils.text_write(f_name, tmp_txt, "")

    # @staticmethod
    # def render(tpl_string, *args, **kwargs):
    #     t = Template(tpl_string)
    #     return t.render(*args, **kwargs)
    #
    # @staticmethod
    # def render_file(file_name, *args, **kwargs):
    #     t = Template(Utils.text_read(file_name))
    #     return t.render(*args, **kwargs)

    @staticmethod
    def get_file_size(file_abs_path):
        """
        返回文件大小
        :param file_abs_path: 文件全路径
        :return: 文件大小，以KB为单位
        """
        st = os.stat(file_abs_path)
        return st.st_size / 1024

    @staticmethod
    def read_excel(excel_file_path, by_name='Sheet1'):

        data = None
        try:
            data = xlrd.open_workbook(excel_file_path)
        except Exception as e:
            print(e)

        table = data.sheet_by_name(by_name)
        nrows = table.nrows
        ncols = table.ncols

        rows = list()
        for rownum in range(1, nrows):
            row = list()
            for colnum in range(0, ncols):
                row.append(table.cell(rownum, colnum).value)
            rows.append(row)

        return rows

    @staticmethod
    def read_excel_sheets(excel_file_path):
        data = None
        try:
            data = xlrd.open_workbook(excel_file_path)
        except Exception as e:
            print(e)
        names = list()
        for sheet in data.sheets():
            names.append(sheet.name)
        return names

    @staticmethod
    def excel_export(handler, html, dwn_file_name):
        handler.set_header("Content-Type", "application/vnd.ms-excel;charset=utf-8")
        handler.add_header("Content-Disposition", "attachment;filename=%s.xls" % dwn_file_name)
        handler.write(html)

    @staticmethod
    def word_export(handler, html, dwn_file_name):
        handler.set_header("Content-Type", "application/ms-word;charset=utf-8")
        handler.add_header("Content-Disposition", "attachment;filename=%s.doc" % dwn_file_name)
        header = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">"
        handler.write(header + html)

    @staticmethod
    def trim(text):
        return "".join(text.split())

    @staticmethod
    def uniq_index():
        return str(uuid.uuid1())

    @staticmethod
    def md5(s):
        h = hashlib.new('ripemd160')
        h.update(bytearray(s.encode("utf8")))
        return h.hexdigest()

    @staticmethod
    def fix_width_num(num, size=3):
        fmt = "{0:0%i}" % size
        return fmt.format(num)

    @staticmethod
    def current_datetime():
        return datetime.now()

    @staticmethod
    def mkdirs(path):
        isexists = os.path.exists(path)
        if not isexists:
            os.makedirs(path)
            return path
        else:
            return path

    @staticmethod
    def parse_int(text):
        nums = Utils.parse_int_array(text)
        if len(nums) > 0:
            return int(nums[0])
        return None

    @staticmethod
    def parse_int_array(text):
        arr = list()
        p = re.compile("[-]?\\d+", re.M)
        nums = p.findall(text)
        if len(nums) > 0:
            arr = [int(s) for s in nums]
        return arr

    @staticmethod
    def parse_time_text(text):
        if not text:
            return ""
        p = re.compile("\\d{2}:\\d{2}")
        dates = p.findall(text)
        if len(dates) > 0:
            return dates[0]
        return ""

    @staticmethod
    def parse_time(text):
        time_text = Utils.parse_time_text(text)
        if not time_text:
            return None
        time_struct = time.strptime(time_text, "%H:%M")
        return datetime.time(time_struct.tm_hour, time_struct.tm_min)

    @staticmethod
    def parse_date_text(text):
        if not text:
            return ""
        p = re.compile("\\d{4}-\\d{2}-\\d{2}")
        dates = p.findall(text)
        if len(dates) > 0:
            return dates[0]
        return ""

    @staticmethod
    def parse_date(text):
        date_text = Utils.parse_date_text(text)
        if not date_text:
            return None
        from datetime import datetime

        return datetime.strptime(date_text, "%Y-%m-%d").date()

    @staticmethod
    def parse_datetime_text(text):
        if not text:
            return ""
        p = "\\d{4}-\\d{2}-\\d{2}\\s{1}\\d{2}:\\d{2}"
        r = re.compile(p)
        matchs = r.findall(text)
        if len(matchs) > 0:
            return matchs[0]
        return ""

    @staticmethod
    def parse_datetime(text):
        datetime_text = Utils.parse_datetime_text(text)
        if not datetime_text:
            return None
        from datetime import datetime

        return datetime.strptime(datetime_text, "%Y-%m-%d %H:%M")

    @staticmethod
    def parse_float(text):
        floats = Utils.parse_float_array(text)
        if len(floats) > 0:
            return float(floats[0])
        else:
            return float(Utils.parse_int(text))

    @staticmethod
    def parse_float_array(text):
        p = re.compile("[-]?\\d+\\.\\d+", re.M)
        return [float(s) for s in p.findall(text)]

    @staticmethod
    def parse_number_array(text):
        """
        int or float
        :param text:
        :return:
        """
        p = re.compile("[-]?\\d+[\\.]?[\\d]*", re.M)
        return [float(s) for s in p.findall(text)]

    @staticmethod
    def encode(obj):
        return json.dumps(obj, cls=JsonEncoder)

    @staticmethod
    def decode(text):
        return json.loads(text)

    @staticmethod
    def obj_to_dict(obj, field_name_arr=None):
        if not field_name_arr:
            return dict()
        tmp = dict()
        for fn in field_name_arr:
            tmp[fn] = getattr(obj, fn)
        return tmp

    @staticmethod
    def matrix_reverse(arr):
        """
        矩阵翻转
        :param arr:
        :return:
        """
        return [[r[col] for r in arr] for col in range(len(arr[0]))]

    @staticmethod
    def combine_text_files(folder, target_file_name):
        text = Utils.text_read(os.path.join(folder, "combine.list"))
        cfg = json.loads(text)
        for key in cfg.keys():
            files = cfg[key]
            if len(files) > 0:
                combine_file = os.path.join(folder, target_file_name + "." + key)
                if os.path.exists(combine_file):
                    os.remove(combine_file)
                all_ = list()
                for file_ in files:
                    path = os.path.join(folder, file_)
                    all_.append(Utils.text_read(path))
                Utils.text_write(combine_file, all_)
        pass

    @staticmethod
    def is_email(s):
        p = r"[^@]+@[^@]+\.[^@]+"
        if re.match(p, s):
            return True
        return False

    @staticmethod
    def email_account_name(s):
        # 匹配@前面的字符串
        p = r".*(?=@)"
        r = re.compile(p)
        matchs = r.findall(s)
        if len(matchs) > 0:
            return matchs[0]
        return ""

    # ########################################## Date Format ######################################################
    @staticmethod
    def timestamp():
        return int(time.mktime(time.localtime()))

    @staticmethod
    def format_year_month(date_obj, split="-"):
        """
        格式化成 yyyy-MM
        :param date_obj: 日期对象
        :param split: 年月分割符
        :return: 格式化后的字符串
        """
        if not date_obj:
            return ""
        return date_obj.strftime('%Y' + split + '%m')

    @staticmethod
    def format_datetime(date_obj, split="-", split2=":", space=" "):
        """
        格式化成 yyyy-MM-dd HH:MM:SS
        :param space: 年月日与时间分割符号
        :param split2: 时间分割符
        :param date_obj: 日期对象
        :param split: 年月日分割符
        :return: 格式化后的字符串
        """
        if not date_obj:
            return ""
        return date_obj.strftime('%Y' + split + '%m' + split + '%d' + space + '%H' + split2 + '%M' + split2 + '%S')

    @staticmethod
    def format_datetime_short(date_obj, split="-", split2=":", space=" "):
        """
        格式化成 yyyy-MM-dd HH:MM
        :param space: 年月日与时间分割符号
        :param split2: 时间分割符
        :param date_obj: 日期对象
        :param split: 年月日分割符
        :return: 格式化后的字符串
        """
        if not date_obj:
            return ""
        return date_obj.strftime('%Y' + split + '%m' + split + '%d' + space + '%H' + split2 + '%M')

    @staticmethod
    def format_date(date_obj, split="-"):
        """
        格式化成 yyyy-MM-dd
        :param date_obj: 日期对象
        :param split: 年月日分割符
        :return: 格式化后的字符串
        """
        if not date_obj:
            return ""
        try:
            return date_obj.strftime('%Y' + split + '%m' + split + '%d')
        except Exception as ex:
            print(ex)
        return ""

    @staticmethod
    def format_time(datetime_obj):
        """
        格式化成 HH:MM
        :param datetime_obj: 日期对象
        :return: 格式化后的字符串
        """
        if not datetime_obj:
            return ""
        import datetime
        if isinstance(datetime_obj, datetime.time):
            curr_date = Utils.current_datetime()
            dt = datetime.datetime.combine(curr_date, datetime_obj)
            return dt.strftime('%H:%M')
        elif isinstance(datetime_obj, datetime.datetime):
            return datetime_obj.strftime('%H:%M')
        return ""

    @staticmethod
    def list_modules(path_):
        """
        得到path_的模块名，模块名包括完整的包名
        :param path_: 扫描的路径
        :return: 模块名列表
        """
        packages = list()
        modules = list()
        iter_files = os.walk(path_)
        for root, dirs, files in iter_files:
            for f in files:
                if f.find('__init__.py') != -1:
                    packages.append(root)

        iter_files = os.walk(path_)
        for root, dirs, files in iter_files:
            for f in files:
                if packages.count(root) == 1 and f.endswith(".py") and f.find('__init__.py') == -1:
                    modules.append(os.path.join(root, f).replace(".py", ""))

        last_modules = list()
        for module in modules:
            tmp = module.replace(path_, "")
            tmp = tmp.replace(os.path.sep, ".")
            last_modules.append(tmp[1:])

        return last_modules

    # ########################################## Date Add ######################################################
    @staticmethod
    def add_days(date, days):
        space = timedelta(days=days)
        return date + space

    # @staticmethod
    # def add_months(date, months):
    #     space = relativedelta(months=months)
    #     return date + space

    @staticmethod
    def add_hours(date, hours):
        space = timedelta(hours=hours)
        return date + space

    @staticmethod
    def add_minutes(date, minutes):
        space = timedelta(minutes=minutes)
        return date + space

    # 友好参数
    @staticmethod
    def pretty_params_encode(v):
        g = v.encode()
        f = base64.encodebytes(g)
        encode_pretty_str = f.decode()
        return encode_pretty_str.replace("\n", "@")

    @staticmethod
    def pretty_params_decode(v):
        g = v.replace("@", "\n").encode()
        f = base64.decodebytes(g)
        return f.decode()