kernels = [
	{
		'name': 'Identity (no filter)',
		'kernel':  [[ 0,  0,  0],
					[ 0,  1,  0],
					[ 0,  0,  0]],
		'factor': 1
	},
	{
		'name': 'Blur (Low Pass)',
		'kernel':  [[ 1,  1,  1],
					[ 1,  1,  1],
					[ 1,  1,  1]],
		'factor': 9
	},
	{
		'name': 'Gaussian Blur',
		'kernel':  [[  1, 2, 1],
					[  2, 4, 2],
					[  1, 2, 1]],
		'factor': 16
	},
	{
		'name': 'Sharpen',
		'kernel':  [[  0, -1,  0],
					[ -1,  5, -1],
					[  0, -1,  0]],
		'factor': 2

	},
	{
		'name': 'High Pass',
		'kernel':  [[ -1, -1, -1],
					[ -1,  8, -1],
					[ -1, -1, -1]],
		'factor': 2
	},
	{
		'name': 'Edge Detection',
		'kernel':  [[ -1, -1, -1],
					[ -1,  9, -1],
					[ -1, -1, -1]],
		'factor': 8
	},
	{
		'name': 'Emboss',
		'kernel':  [[ -2, -1,  0],
					[ -1,  1,  1],
					[  0,  1,  2]],
		'factor': 2

	}
]