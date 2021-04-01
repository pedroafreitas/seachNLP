import argparse
import model
import sys
import util

def parseArgs():
    p = argparse.ArgumentParser()
    p.add_argument('--text-corpus', help='Treinando a partir do curpus corpus')
    p.add_argument('--model', help='Sempre use esse modelo')
    return p.parse_args()

def selectLanguage():
    corpus = ''
    while (corpus != 'eng' and corpus != 'ger' and corpus != 'chi' and corpus != 'por'):
        print('\nSelecione um idioma: eng, por, chi, ger')
        sys.stdout.write('>> ')
        corpus = sys.stdin.readline().strip()    
        if corpus == 'eng':
            corpus = 'leo.txt'
            return corpus
        elif corpus == 'por':
            corpus = 'machado.txt'
            return corpus
        elif corpus == 'ger':
            corpus = 'nieuwenhuis.txt'
            return corpus
        print('\nTemos Por, Eng, Ger e Chi')

# REPL and main entry point
def repl(unigramCost, bigramCost, possibleFills, command=None):
    '''REPL: read, evaluate, print, loop'''

    while True:
        sys.stdout.write('>> ')
        line = sys.stdin.readline().strip()
        if not line:
            break

        if command is None:
            cmdAndLine = line.split(None, 1)
            cmd, line = cmdAndLine[0], ' '.join(cmdAndLine[1:])
        else:
            cmd = command
            line = line

        print('')
        
        if cmd == 'help':
            print('Usage: <command> [arg1, arg2, ...]')
            print('')
            print('Commands:')
            print(('\n'.join(a + '\t\t' + b for a, b in [
                ('help', 'Ajuda'),
                ('corpus', 'Muda o corpus - idioma'),
                ('seg', 'Segmentar Strings'),
                ('ins', 'Inserir Vogais'),
                ('fills', 'Query possibleFills() para ver as vogais possiveis para preencher uma palavra'),
                ('ug', 'Query a funcao de custo unigrama. Trata o input como unico'),
                ('bg', 'Query a funcao bigrama das ultimas duas palavras que foram colocadas como input'),
            ])))
            print('')
            print('Insira uma linha vazia para sair')

        elif cmd == 'corpus':
            selectLanguage()
        elif cmd == 'seg':
            line = util.cleanLine(line)
            parts = util.words(line)
            print(('  Query (seg):', ' '.join(parts)))
            print('')
            print(('  ' + ' '.join(
                model.segmentWords(part, unigramCost) for part in parts)))

        elif cmd == 'ins':
            line = util.cleanLine(line)
            ws = [util.removeAll(w, 'aeiou') for w in util.words(line)]
            print(('  Query (ins):', ' '.join(ws)))
            print('')
            print(('  ' + model.insertVowels(ws, bigramCost, possibleFills)))

        elif cmd == 'fills':
            line = util.cleanLine(line)
            print(('\n'.join(possibleFills(line))))

        elif cmd == 'ug':
            line = util.cleanLine(line)
            print((unigramCost(line)))

        elif cmd == 'bg':
            grams = tuple(util.words(line))
            prefix, ending = grams[-2], grams[-1]
            print((bigramCost(prefix, ending)))

        else:
            print(('Comando nao reconhecido:', cmd))

        print('')

def main():
    args = parseArgs()
    corpus = selectLanguage()


    if args.model and args.model not in ['seg', 'ins', 'both']:
        print(('Modelo não reconhecido:', args.model))
        sys.exit(1)


    sys.stdout.write('Treinando as funcoes de custo [corpus: %s]... ' % corpus)
    sys.stdout.flush()

    unigramCost, bigramCost = util.makeLanguageModels(corpus)
    possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

    print('Pronto!')
    print('')

    repl(unigramCost, bigramCost, possibleFills, command=args.model)
