class Error:
    def __init__(self, title, details, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_title = title
        self.details = details

    def __repr__(self):
        res = f'{self.error_title}\n'
        res += f':{self.pos_start.line + 1} הרושב {self.pos_start.file_name} :ץבוקב הז\n'
        res += f'{self.details}'
        return res
class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end): 
        super().__init__(" ינלאמש הזה ותה ,םירקי םיחרזא", details, pos_start, pos_end)
class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("הזה חוסינה תא ןיבמ אל ינא יכ ,רפסה תיבל רוזחתש יאדכ דיפל", details, pos_start, pos_end)
