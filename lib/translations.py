import bpy

keys = [
    {
        "context": "Operator",
        "key": "Operator ",
        "ja_JP": "オペレータ 1",
    },
    {
        "context": "*",
        "key": "description",
        "ja_JP": "説明",
    },
]


def get_dict():
    translation_dict = {
        "en_US": {(v["context"], v["key"]): v["key"] for v in keys},
        "ja_JP": {(v["context"], v["key"]): v["ja_JP"] for v in keys},
    }
    return translation_dict


def register():
    transration_dict = get_dict()
    bpy.app.translations.register(__name__, transration_dict)


def unregister():
    bpy.app.translations.unregister(__name__)
