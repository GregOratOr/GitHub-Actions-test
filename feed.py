import yaml
import xml.etree.ElementTree as xmlTree
from pathlib import Path


feed_path = Path("feed.yaml")

with feed_path.open('r') as file:
    yaml_data = yaml.safe_load(file)
    
    rss_dict = {
        'version':'2.0',
        'xmlns:itunes':'https://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content':'https://purl.org/rss/1.0/modules/content/'
    }

    rss_element = xmlTree.Element('rss', rss_dict)


    channel_element = xmlTree.SubElement(rss_element, 'channel')

    link_prefix = yaml_data['link']

    xmlTree.SubElement(channel_element, 'title').text = yaml_data['title']
    xmlTree.SubElement(channel_element, 'format').text = yaml_data['format']
    xmlTree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    xmlTree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xmlTree.SubElement(channel_element, 'description').text = yaml_data['description']
    xmlTree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
    xmlTree.SubElement(channel_element, 'language').text = yaml_data['language']
    xmlTree.SubElement(channel_element, 'link').text = link_prefix
    # xmlTree.SubElement(channel_element, 'link', {'href':link_prefix})

    xmlTree.SubElement(channel_element, 'itunes:category', {'text': link_prefix + yaml_data['category']})
    for item in yaml_data['item']:
        item_element = xmlTree.SubElement(channel_element, 'item')
        xmlTree.SubElement(item_element, 'title').text = item['title']
        xmlTree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xmlTree.SubElement(item_element, 'description').text = item['description']
        xmlTree.SubElement(item_element, 'pubDate').text = item['published']
        xmlTree.SubElement(item_element, 'itunes:duration').text = item['duration']

        enclosure = xmlTree.SubElement(item_element, 'enclosure', {'url': link_prefix + item['file'],
                                                                  'type': 'audio/mpeg',
                                                                  'length': item['length']})


    output_tree = xmlTree.ElementTree(rss_element)

    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)




