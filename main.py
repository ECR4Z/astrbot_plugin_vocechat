# my_vocechat_plugin/main.py

from astrbot.api.star import Context, Star, register

@register(
    name="vocechat_plugin_main",
    author="HikariFroya",
    desc="VoceChat 平台适配器加载插件", 
    version="1.0.0"
)
class VoceChatPluginStar(Star):
    def __init__(self, context: Context):
        super().__init__(context) 

        from .vocechat_adapter import VoceChatAdapter  # noqa: F401
        if hasattr(self, 'logger') and self.logger is not None:
            self.logger.info("VoceChatPluginStar (Star Component) 初始化成功 (使用 self.logger)。VoceChatAdapter 已被导入。")
        else:
            print("[INFO] VoceChatPluginStar (Star Component) initialized. VoceChatAdapter should be imported and registered.")
