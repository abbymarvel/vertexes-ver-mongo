from collections import defaultdict


def clean_chars(string):
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("'", "")
    return string


def process_link_line(line):
    tokens = line.split("(")
    el1 = tokens[2]
    rel = tokens[3]
    el2 = tokens[4]
    el1 = clean_chars(el1)
    rel = clean_chars(rel)
    el2 = clean_chars(el2)
    el1_tokens = el1.split(",")
    rel_tokens = rel.split(",")
    el2_tokens = el2.split(",")
    db_name1 = el1_tokens[0]
    source_name1 = el1_tokens[1]
    attr_name1 = el1_tokens[2]
    rel_name = rel_tokens[0]
    rel_url = rel_tokens[1]
    db_name2 = el2_tokens[0]
    source_name2 = el2_tokens[1]
    attr_name2 = el2_tokens[2]
    class1 = el2_tokens[3]
    class2 = el2_tokens[4]
    return ((db_name1, source_name1, attr_name1), (rel_name), (db_name2, source_name2, attr_name2), (class1, class2))


def draw_links_from_group(path):
    attrclass = defaultdict(lambda: defaultdict(int))
    classattr = defaultdict(lambda: defaultdict(int))

    with open(path, 'r') as f:
        for l in f:
            sch1, rel, sch2, cla = process_link_line(l)
            class1, class2 = cla
            _, _, attr1 = sch1
            _, _, attr2 = sch2
            class1 = class1.rstrip()
            class2 = class2.rstrip()
            attr1 = attr1.rstrip()
            attr2 = attr2.rstrip()
            attrclass[attr1][class1] += 1
            attrclass[attr2][class2] += 1
            classattr[class1][attr1] += 1
            classattr[class2][attr2] += 1
    chosen_pairs = set()
    for k, v in attrclass.items():
        choice = ""
        max_v = 9999999
        for k2, v2 in v.items():
            if v2 < max_v:
                max_v = v2
                choice = k2
        chosen_pairs.add((k, choice))
    for k, v in classattr.items():
        choice = ""
        max_v = 0
        for k2, v2 in v.items():
            if v2 > max_v:
                max_v = v2
                choice = k2
        chosen_pairs.add((choice, k))
    print(str(len(chosen_pairs)))
    with open(path, 'r') as f:
        selected_links = set()
        selected_and_drawn = set()
        seen = set()
        for l in f:
            sch1, rel, sch2, cla = process_link_line(l)
            class1, class2 = cla
            _, _, attr1 = sch1
            _, _, attr2 = sch2
            class1 = class1.rstrip()
            class2 = class2.rstrip()
            attr1 = attr1.rstrip()
            attr2 = attr2.rstrip()

            if (attr1, class1) in chosen_pairs and (attr2, class2) in chosen_pairs:
                selected_links.add(l)
                if (class1, class2) not in seen:
                    selected_and_drawn.add(l)
                seen.add((class1, class2))

    print("Total filtered links: " + str(len(selected_links)))
    for el in selected_links:
        print(str(el))
    print("Total filtered-drawn links: " + str(len(selected_and_drawn)))
    for el in selected_and_drawn:
        print(str(el))


if __name__ == "__main__":
    print("processor")
    #
    draw_links_from_group("/Users/ra-mit/Downloads/match_and_links/links_dlc_sem")

    exit()

    with open("/Users/ra-mit/Downloads/match_and_links/links_dlc_sem", 'r') as f:
        total_lines = 0
        counter_concept = defaultdict(int)
        counter_sch_attr = defaultdict(int)
        counter_attr = defaultdict(int)
        test = defaultdict(lambda: defaultdict(int))
        test2 = defaultdict(lambda: defaultdict(int))
        links_without_modified_data = 0
        for l in f:
            total_lines += 1
            sch1, rel, sch2, cla = process_link_line(l)
            # Count co-occurrences of concepts
            class1, class2 = cla
            _, _, attr1 = sch1
            _, _, attr2 = sch2
            class1 = class1.rstrip()
            class2 = class2.rstrip()
            attr1 = attr1.rstrip()
            attr2 = attr2.rstrip()
            key = class1 + class2
            key_attr = attr1 + attr2
            counter_concept[key] += 1
            counter_sch_attr[key_attr] += 1
            counter_attr[attr1] += 1
            counter_attr[attr2] += 1

            test[attr1][class1] += 1
            test2[class1][attr1] += 1
            test[attr2][class2] += 1
            test2[class2][attr2] += 1

            if class1.find("Spvs") != -1 and class2.find("Summary_Protocol_Variant_Set") != -1:
                print(l)

            # if attr1.find("MODIFIED_DATE") == -1 and attr2.find("MODIFIED_DATE") == -1:
            #     links_without_modified_data += 1
            #     nlink = str(sch1) + " - " + str(rel) + " - " + str(sch2)
            #     print(nlink)
        print("Total lines: " + str(total_lines))
        ord = sorted(counter_concept.items(), key=lambda x: x[1], reverse=True)
        ord_sch_attr = sorted(counter_sch_attr.items(), key=lambda x: x[1], reverse=True)
        ord_attr = sorted(counter_attr.items(), key=lambda x: x[1], reverse=True)
        for el in ord:
            print(str(el))
        # for el in ord_sch_attr:
        #     print(str(el))
        # for el in ord_attr:
        #     print(str(el))
        print("rem: " + str(links_without_modified_data))

