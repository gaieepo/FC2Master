# -*- coding: utf-8 -*-
import scrapy
from test_project.items import VideoItem


class FC2Spider(scrapy.Spider):
    name = "fc2"
    allowed_domains = ["fc2.com"]

    def start_requests(self):
        base_url = 'http://video.fc2.com/en/a/list.php?page=%s&m=cat_top&sobj_up_mt_code=19'
        for page in range(1, 10):
            url = base_url % page
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        videos = response.css('div#video_list_1column div.video_list_renew')
        for video in videos:
            video_item = VideoItem()
            video_item['vid'] = video.css('div.video_info_right h3 a::attr(href)').re(
                r'http://video.fc2.com/en/a/content/(.*)/')[0]
            video_item['title'] = video.css(
                'div.video_info_right h3 a::text').extract_first()
            video_item['img_src'] = video.css(
                'img.img::attr(src)').extract_first()
            video_item['duration'] = video.css(
                'span.video_time_renew::text').extract_first()
            video_item['permission'] = video.css(
                'li.member_icon::text').extract_first()
            video_item['view_count'] = int(video.xpath(
                '//li[child::img[@class="icon_views"]]/text()').extract_first())
            video_item['comment_count'] = int(
                video.css('img.icon_comments+a::text').extract_first())
            star_src = video.css('li.recommend')[0]
            video_item['star_count'] = len(
                star_src.css('img.icon_star')) * 1.0 + len(star_src.css('img.icon_star_half')) * 0.5
            video_item['user_id'] = video.css('p.user_name a::attr(href)').re(
                r'http://video.fc2.com/en/a/member\?mid=(.*)')[0]
            yield video_item
