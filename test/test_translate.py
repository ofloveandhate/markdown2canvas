import sys
sys.path.insert(0,'../')

import markdown2canvas


sources = ['plain_text','has_local_images']

for s in sources:
	with open(f'{s}/result.html','w') as result:
		result.write(markdown2canvas.markdown2html(f'{s}/source.md'))


