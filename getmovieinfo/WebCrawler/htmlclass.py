from abc import abstractmethod, ABCMeta


class getVideoInfoBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.info = VideoInfo()

    def getVideoInfo(self,lx):
        self.info['title'] = self.getTitle(lx)
        if self.info['title']:
            self.info['studio'] = self.getStudio(lx)
            self.info['year'] = self.getYear(lx)
            self.info['outline'] = self.getOutline(lx)
            self.info['runtime'] = self.getRuntime(lx)
            self.info['director'] = self.getDirector(lx)
            self.info['actor'] = self.getActor(lx)
            self.info['release'] = self.getRelease(lx)
            self.info['number'] = self.getNum(lx)
            self.info['cover'] = self.getCover(lx)
            self.info['imagecut'] = 1
            self.info['tag'] = self.getTag(lx)
            self.info['extrafanart'] = self.getExtrafanart(lx)
            self.info['label'] = self.getSeries(lx)
            self.info['download'] = self.getMagnetLink(lx)

    @abstractmethod
    def getMagnetLink(self,html):
        pass
    @abstractmethod
    def getActorPhoto(self,html):
        pass
    @abstractmethod
    def getTitle(self,html):  #获取标题
        pass
    @abstractmethod
    def getStudioJa(self,html):
        pass
    @abstractmethod
    def getStudio(self,html): #获取厂商
        pass
    @abstractmethod
    def getYear(self,html):   #获取年份
        pass
    @abstractmethod
    def getCover(self,html):  #获取封面链接
        pass
    @abstractmethod
    def getRelease(self,html): #获取出版日期
        pass
    @abstractmethod
    def getRuntime(self,html): #获取分钟 已修改
        pass
    @abstractmethod
    def getActor(self,html):   #获取女优
        pass
    @abstractmethod
    def getNum(self,html):     #获取番号
        pass
    @abstractmethod
    def getDirectorJa(self,html):
        pass
    @abstractmethod
    def getDirector(self,html): #获取导演
        pass
    @abstractmethod
    def getCID(self,html):
        pass
    @abstractmethod
    def getOutline(self,html):  #获取剧情介绍 多进程并发查询
        pass
    @abstractmethod
    def getSeriesJa(self,html):
        pass
    @abstractmethod
    def getSeries(self,html):   #获取系列
        pass
    @abstractmethod
    def getTag(self,html):  # 获取标签
        pass
    @abstractmethod
    def getExtrafanart(self,html):  # 获取剧照
        pass

class VideoDownloadInfo(dict):
    FIELDS = [
        'title',
        'size',
        'date',
        'isHD',
        'isChn',
        'magnetlink'
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self['title'] = ''
        self['size'] = ''
        self['date'] = ''
        self['isHD'] = 0
        self['isChn'] = 0
        self['magnetlink'] = ''
        for k, v in kwargs:
            if k in self.FIELDS:
                self[k] = v

    
class VideoInfo(dict):
    FIELDS=[
        'title',
        'studio',
        'year',
        'outline',
        'runtime',
        'director',
        'actor',
        'release',
        'number',
        'cover',
        'imagecut',
        'tag',
        'extrafanart',
        'label',
        #'actor_photo',
        'website',
        'source',
        'series',
        'download'
    ]
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self['title'] = ''
        self['studio'] = ''
        self['year'] = ''
        self['outline'] = ''
        self['runtime'] = ''
        self['director'] = ''
        self['actor'] = ''
        self['release'] = ''
        self['number'] = ''
        self['cover'] = ''
        self['imagecut'] = ''
        self['tag'] = ''
        self['extrafanart'] = ''
        self['label'] = ''
        #self['actor_photo'] = ''
        self['website'] = ''
        self['source'] = ''
        self['series'] = ''
        self['download'] = ''
        for k, v in kwargs:
            if k in self.FIELDS:
                self[k] = v

