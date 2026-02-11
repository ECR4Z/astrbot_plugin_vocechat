# vocechat_event.py
from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.platform import AstrBotMessage, PlatformMetadata, MessageType # 确保 MessageType 被导入
from astrbot import logger 
from astrbot.api.message_components import Plain
from typing import TYPE_CHECKING

# 从正确的位置导入 MessageSesion (单s)
from astrbot.core.platform.astr_message_event import MessageSesion 

if TYPE_CHECKING: 
    # 为了类型提示，我们向前声明 VoceChatAdapter
    # 实际的导入由 vocechat_adapter.py 完成，以避免循环导入问题
    from .vocechat_adapter import VoceChatAdapter


class VoceChatEvent(AstrMessageEvent):
    adapter: 'VoceChatAdapter' # 类型提示，实际在 __init__ 中赋值

    def __init__(self, message_obj: AstrBotMessage, platform_meta: PlatformMetadata, adapter_instance: 'VoceChatAdapter'):
        # --- 从 message_obj 中获取 message_str 和 session_id ---
        message_str_for_event = ""
        # 尝试从 message_obj.message_str 获取
        if hasattr(message_obj, 'message_str') and message_obj.message_str is not None:
            message_str_for_event = message_obj.message_str
        # 如果 message_str 为空，但 message 列表不为空，尝试从第一个 Plain 组件获取
        elif message_obj.message and isinstance(message_obj.message, list) and len(message_obj.message) > 0:
            first_segment = message_obj.message[0]
            if isinstance(first_segment, Plain):
                message_str_for_event = first_segment.text
            else:
                # 如果第一个元素不是 Plain，可以简单地用组件类型作为占位符
                message_str_for_event = f"[{type(first_segment).__name__} ...]" 
        else:
            logger.debug("VoceChatEvent: message_obj 中无法提取有效的 message_str")

        session_id_for_event = "unknown_session"
        # 优先使用 message_obj 中由适配器 convert_message 设置的 session_id
        if hasattr(message_obj, 'session_id') and message_obj.session_id is not None:
            session_id_for_event = message_obj.session_id
        # 如果没有，根据消息类型回退到 group_id 或 user_id
        elif hasattr(message_obj, 'type'):
            if message_obj.type == MessageType.GROUP_MESSAGE and hasattr(message_obj, 'group_id') and message_obj.group_id:
                 session_id_for_event = message_obj.group_id
            elif message_obj.type == MessageType.FRIEND_MESSAGE and hasattr(message_obj, 'sender') and message_obj.sender:
                 session_id_for_event = message_obj.sender.user_id
            elif hasattr(message_obj, 'sender') and message_obj.sender: # 作为最后的备选
                 session_id_for_event = message_obj.sender.user_id
            else:
                logger.warning("VoceChatEvent: message_obj 中无法提取有效的 session_id (user_id/group_id 也缺失或类型不符)")
        else:
            logger.warning("VoceChatEvent: message_obj 中缺少 type 属性，无法准确判断 session_id")
        
        # 调用父类的 __init__ 方法
        # 它会自动根据 platform_meta.name, message_obj.type, session_id_for_event 创建 self.session (MessageSesion 类型)
        super().__init__(
            message_str=message_str_for_event,
            message_obj=message_obj,
            platform_meta=platform_meta,
            session_id=session_id_for_event
        )
        
        self.adapter = adapter_instance # 保存适配器实例，以便 send 方法调用

    async def send(self, message_chain: MessageChain):
        logger.info(f"VoceChatEvent.send() 被调用，准备通过适配器发送消息。Event Session (self.session): {self.session}")
        
        if hasattr(self, 'adapter') and self.adapter:
            # AstrMessageEvent 基类的 __init__ 已经创建了 self.session，其类型为 MessageSesion (单s)。
            # VoceChatAdapter 的 send_by_session 方法参数 session 也期望是 MessageSesion 类型。
            # 所以我们直接传递 self.session。
            await self.adapter.send_by_session(
                session=self.session, # <--- 使用由基类创建的 self.session (MessageSesion 类型)
                message_chain=message_chain
            )
            logger.info(f"VoceChatEvent.send(): 消息已尝试通过适配器发送。")
        else:
            logger.error("VoceChatEvent.send(): 无法发送消息，因为 adapter 实例未设置！")
        
        # 仍然可以调用 super().send() 来执行 AstrMessageEvent 基类中 send 方法的逻辑
        # (例如，它可能会做一些统计或标记操作)
        await super().send(message_chain)

