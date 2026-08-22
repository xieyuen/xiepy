from typing import Iterable, Self

import mcdreforged as mcdr


class TranslationItem:
    """MCDR 翻译键

    用于封装翻译键的类, 提供便捷的翻译文本获取方法.

    一般来说, 在 MCDR 插件中获取翻译是通过 ``ServerInterface.tr()`` 和 ``ServerInterface.rtr()``
    获取的, 并且需要手动填入 key, 容易打错. 所以我设计了这个类, 让 IDE 有更好的提示.

    一般的使用方法是定义一个翻译键集合类, 然后把所有的翻译键放进来

    >>> class TranslationKeys:
    ...     a_simple_key = TranslationItem("plugin_id.a_simple_key")
    ...     green_text_key = TranslationItem("plugin_id.green_text_key").set_color(mcdr.RColor.green)
    ...     a_complex_key = TranslationItem("plugin_id.a_complex_key")

    然后在代码中就可以使用

    >>> TranslationKeys.a_complex_key.rtr()

    直接获取翻译对象还不怕写错字

    Attributes:
        key (str): 完整的翻译键
    """

    server: mcdr.ServerInterface | None = mcdr.ServerInterface.si_opt()

    def __init__(self, translation_key: str):
        self.key = translation_key
        self.color = None
        self.styles = None
        self.click_event = None
        self.hover = None

    def tr(self, *args, **kwargs) -> str | mcdr.RTextBase:
        assert self.server is not None
        return self.server.tr(self.key, *args, **kwargs)

    def rtr(self, *args, **kwargs) -> mcdr.RTextMCDRTranslation:
        assert self.server is not None
        return self.__apply(self.server.rtr(self.key, *args, **kwargs))

    def set_color(self, color: mcdr.RColor) -> Self:
        self.color = color
        return self

    def set_styles(self, styles: mcdr.RStyle | Iterable[mcdr.RStyle]) -> Self:
        self.styles = styles
        return self

    def set_click_event(self, *args, **kwargs) -> Self:
        """参数的填写与 ``RTextBase.set_click_event()`` 相同"""
        self.click_event = args, kwargs
        return self

    def set_hover_text(self, *texts) -> Self:
        self.hover = texts
        return self

    def __apply[T: mcdr.RTextBase](self, rtext: T) -> T:
        if self.color:
            rtext.set_color(self.color)
        if self.styles:
            rtext.set_styles(self.styles)
        if self.click_event:
            args, kwargs = self.click_event
            rtext.set_click_event(*args, **kwargs)
        if self.hover:
            rtext.set_hover_text(self.hover)

        return rtext
