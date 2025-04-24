from textpy.jit import text

@text(cache=None)
def translate_text_to_Chinese(*, src: str,tgt:str) -> str: ...

def get_src_text():
    return "The quantum entanglement phenomenon challenges classical physics concepts."

if __name__ == "__main__":
    source_text = get_src_text()
    tgt_language = "Japan"
    target_text = translate_text_to_Chinese(src = source_text,tgt = tgt_language)
    print(target_text)
