#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


def find_ftln(play_file):

    tree = ET.parse(play_file)
    root = tree.getroot()
    namespace_milestone = '{http://www.tei-c.org/ns/1.0}milestone'
    namespace_id = '{http://www.w3.org/XML/1998/namespace}id'
    scene_act_line_ftln = []
    for child in root.iter(namespace_milestone):
        if child.attrib['n'].startswith('P') or 'CHO' in child.attrib['n']:
            continue
        if (child.attrib[namespace_id].startswith('ms') or
                child.attrib[namespace_id].startswith('stz')):
            continue
        scene_act_line_ftln.append([child.attrib['n'],
                                    child.attrib[namespace_id]])

    return scene_act_line_ftln


def main():

    play_file = 'Rom.xml'
    scene_act_line_ftln = find_ftln(play_file)

    with open('si601_hw3_part1_output_leabbott.txt', 'wb') as f:
        for line in scene_act_line_ftln:
            f.write('\t'.join(line) + '\n')


if __name__ == '__main__':
    main()
