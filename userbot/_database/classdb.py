from . import pdB

class AFK(object):
    """AMC -> Afk Modification Class"""

    def set_afk(self, afk, reason, afktime):
        afk_db = pdB.get_key("AFK_DB") or []
        if afk_db:
            pdB.del_key("AFK_DB")
        pdB.set_key("AFK_DB", [afk, reason, afktime])
        
    
    def get_afk():
        afk = pdB.get_key("AFK_DB")
        if afk:
            return afk[0], afk[1], afk[2]
        return False

    
            



class WELCOME():
    try:
        pdB.get_key("WELCOME") or {}
    except BaseException:
        pdB.set_key("WELCOME", "{}")

    def set_welcome(self, chat_id, file_id, text=None):
        ok = pdB.get_key("WELCOME")
        ok.update({chat_id: {"file_id": file_id, "caption": text}})
        return pdB.set_key("WELCOME", ok)

    def get_welcome(self, chat_id):
        ok = pdB.get_key("WELCOME")
        wl = ok.get(chat_id)
        if wl:
            return wl
        return


    def del_welcome(self, chat_id):
        ok = pdB.get_key("WELCOME")
        wl = ok.get(chat_id)
        if wl:
            ok.pop(chat_id)
            return pdB.set_key("WELCOME", ok)
        return

    def get_welcome_ids(self):
        chat_ids = []
        all_welcome = pdB.get_key("WELCOME") or {}
        for x in all_welcome:
            if not (int(x.chat_id) in chat_ids):
                chat_ids.append(int(x.chat_id))
        return chat_ids


class DV():
    setdv = pdB.set_key
    getdv = pdB.get_key
    deldv = pdB.del_key

    def getalldv(self):
        kv_data = {}
        mydata = pdB.get_key
        for x in mydata:
            kv_data.update({x.keys: x.values})

        return kv_data



class Database(DV, WELCOME, AFK):
    pass
