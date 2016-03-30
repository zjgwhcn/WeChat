import os


class Config:
    # 配置url地址及一些常量值
    APP_ID = os.environ.get('APP_ID')
    APP_SECRET = os.environ.get('APP_SECRET')
    URL_PIC_DOWNLOAD = 'http://192.168.199.135:8080/?action=snapshot'

    # 需要格式化appid和secret
    URL_ACESSTOKEN = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'

    # 需要格式化uaaccess_token
    URL_OPENID = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid'
    URL_CUSTOMER_SERVICE = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'
    URL_PIC_UPLOAD = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
