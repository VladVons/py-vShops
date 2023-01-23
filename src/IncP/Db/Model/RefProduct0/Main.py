from IncP.Db.Model import TModel


class TMain(TModel):
    def _GetConf(self) -> dict:
        return {
            'masters': {
                'ref_product0': 'id'
            },
            'param': {
                'ref_product0_crawl': 'crawl_site_id',
                'ref_product0_to_category': 'category_id',
                'ref_product0_lang': 'lang_id'
            }
        }
