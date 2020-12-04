
document_structure_elements_set = set([
	'body',
	'head',
	'html',
])
document_head_elements_set = set([
	'base',
	'basefont',
	'isindex',
	'link',
	'meta',
	'object',
	'script',
	'style',
	'title',
])
document_body_elements_set = set([
	'a',
	'abbr',
	'acronym',
	'address',
	'applet',
	'area',
	'article',
	'aside',
	'audio',
	'b',
	'bdi',
	'bdo',
	'big',
	'blockquote',
	'br',
	'button',
	'canvas',
	'caption',
	'center',
	'cite',
	'code',
	'col',
	'colgroup',
	'data',
	'datalist',
	'dd',
	'del',
	'dfn',
	'dir',
	'div',
	'dl',
	'dt',
	'em',
	'embed',
	'fieldset',
	'figcaption',
	'figure',
	'font',
	'footer',
	'form',
	'h1',
	'h2',
	'h3',
	'h4',
	'h5',
	'h6',
	'header',
	'hr',
	'i',
	'img',
	'input',
	'ins',
	'isindex',
	'kbd',
	'keygen',
	'label',
	'legend',
	'li',
	'main',
	'map',
	'mark',
	'menu',
	'meter',
	'nav',
	'noscript',
	'object',
	'ol',
	'optgroup',
	'option',
	'output',
	'p',
	'param',
	'pre',
	'progress',
	'q',
	'rb',
	'rp',
	'rt',
	'rtc',
	'ruby',
	's',
	'samp',
	'script',
	'section',
	'select',
	'small',
	'source',
	'span',
	'strike',
	'strong',
	'sub',
	'sup',
	'table',
	'tbody',
	'td',
	'template',
	'textarea',
	'tfoot',
	'th',
	'thead',
	'time',
	'tr',
	'track',
	'tt',
	'u',
	'ul',
	'var',
	'video',
	'wbr',
	])
block_elements_set = set([
		'address',
		'article',
		'aside',
		'blockquote',
		'center',
		'dd',
		'del',
		'dir',
		'div',
		'dl',
		'dt',
		'figcaption',
		'figure',
		'footer',
		'h1',
		'h2',
		'h3',
		'h4',
		'h5',
		'h6',
		'header',
		'hr',
		'ins',
		'li',
		'main',
		'menu',
		'nav',
		'noscript',
		'ol',
		'p',
		'pre',
		'script',
		'section',
		'ul',
		])
basic_text_set = set([
			'h1',
			'h2',
			'h3',
			'h4',
			'h5',
			'h6',
			'p',
		])
section_headings_set = set([
			'h1',
			'h2',
			'h3',
			'h4',
			'h5',
			'h6',
		])
lists_set = set([
			'dd',
			'dir',
			'dl',
			'dt',
			'li',
			'ol',
			'ul',
		])
other_block_elements_set = set([
			'address',
			'article',
			'aside',
			'blockquote',
			'center',
			'del',
			'div',
			'figcaption',
			'figure',
			'footer',
			'header',
			'hr',
			'ins',
			'main',
			'menu',
			'nav',
			'noscript',
			'pre',
			'script',
			'section',
	])
inline_elements_set = set([
		'a',
		'abbr',
		'acronym',
		'b',
		'bdi',
		'bdo',
		'big',
		'br',
		'cite',
		'code',
		'data',
		'del',
		'dfn',
		'em',
		'font',
		'i',
		'ins',
		'kbd',
		'mark',
		'q',
		'rb',
		'rp',
		'rt',
		'rtc',
		'ruby',
		's',
		'samp',
		'script',
		'small',
		'span',
		'strike',
		'strong',
		'sub',
		'sup',
		'template',
		'time',
		'tt',
		'u',
		'var',
		'wbr',
		])
anchor_set = set([
			'a',
		])
phrase_elements_set = set([
			'abbr',
			'acronym',
			'b',
			'big',
			'code',
			'dfn',
			'em',
			'font',
			'i',
			'kbd',
			's',
			'samp',
			'small',
			'strike',
			'strong',
			'tt',
			'u',
			'var',
			])
general_set = set([
				'abbr',
				'acronym',
				'dfn',
				'em',
				'strong',
			])
computer_phrase_elements_set = set([
				'code',
				'kbd',
				'samp',
				'var',
			])
presentation_set = set([
				'b',
				'big',
				'font',
				'i',
				's',
				'small',
				'strike',
				'tt',
				'u',
		])
span_set = set([
			'span',
		])
other_inline_elements_set = set([
			'bdi',
			'bdo',
			'br',
			'cite',
			'data',
			'del',
			'ins',
			'mark',
			'q',
			'rb',
			'rp',
			'rt',
			'rtc',
			'ruby',
			'script',
			'sub',
			'sup',
			'template',
			'time',
			'wbr',
	])
images_and_objects_set = set([
		'applet',
		'area',
		'audio',
		'canvas',
		'embed',
		'img',
		'map',
		'object',
		'param',
		'source',
		'track',
		'video',
	])
forms_set = set([
		'button',
		'datalist',
		'fieldset',
		'form',
		'input',
		'isindex',
		'keygen',
		'label',
		'legend',
		'meter',
		'optgroup',
		'option',
		'output',
		'progress',
		'select',
		'textarea',
	])
tables_set = set([
		'caption',
		'col',
		'colgroup',
		'table',
		'tbody',
		'td',
		'tfoot',
		'th',
		'thead',
		'tr',
])
frames_set = set([
	'frame',
	'frameset',
	'iframe',
	'noframes',
	])
historic_elements_set = set([
	'listing',
	'nextid',
	'plaintext',
	'xmp',
])
non_standard_elements_set = set([
	'blink',
	'layer',
	'marquee',
	'nobr',
	'noembed',
])