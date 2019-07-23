class LogicManager():

    def keyword_data_transformer(self, lab_data, ad_data, source="Naver"):
        rel_sum = 0
        for d in lab_data['results'][0]['data']:
            rel_sum += d['ratio']
        abs_sum = ad_data['monthlyPcQcCnt'] + ad_data['monthlyMobileQcCnt']

        result = {}
        result['date'] = lab_data['results'][0]['data'][-1]['period'].replace('-', '')
        result['source'] = source
        result['keyword'] = ad_data['relKeyword']
        result['query'] =  round(abs_sum / rel_sum * lab_data['results'][0]['data'][-1]['ratio'])
        return result

#logic = LogicManager()
#result = logic.keyword_data_transformer(lab_data, ad_data, source="Naver")