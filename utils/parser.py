

class LabeledFileParser(object):
    def __init__(self):
        super(LabeledFileParser, self).__init__()

    def parse(self, labeled_file):
        try:
            labels = []
            fp = open(labeled_file, 'r')
            tmp = []
            record = ''
            for line in fp:
                if len(line.strip()) == 0:  #empty line
                    if tmp:
                        labels.append((record,tmp))
                        record = ''
                        tmp = []
                elif len(line.split()) > 5: #record itself
                    record = line
                else:   #tokens and their labels
                    label = line.split()[-1].strip()
                    tmp.append(label)
            fp.close()
            return labels
        except Exception, e:
            raise e
        