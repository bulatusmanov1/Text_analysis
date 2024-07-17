const NUM_TESTS = 362
# max number of answers returned per test
const NUM_RESULTS = 10
# total number of correct answers for all tests
const TRUES = 691

export def stats [cutoff] {
	let tests = $in

	mut tp = 0
	mut fp = 0

	for test in $tests {
		for $result in $test {
			if $result.1 < $cutoff {
				break
			}

			if $result.0 == null {
				continue
			}

			if $result.0 <= 4 {
				$tp += 1
			} else {
				$fp += 1
			}
		}
	}

	{
		tp: $tp
		fp: $fp
		tn: ($NUM_TESTS * $NUM_RESULTS - $TRUES - $fp)
		fn: ($TRUES - $tp)
	}
}

export def metrics [] {
	{
		precision: ($in.tp / ($in.tp + $in.fp))
		recall: ($in.tp / $TRUES)
	}
}

export def cutoffs [] {
	let data = $in

	0.3..0.31..<0.76
		| each {|cutoff|
			let metrics = $data | stats $cutoff | metrics

			{
				cutoff: $cutoff
				...$metrics
			}
		}
		| insert f { f --beta 0.3 }
}

export def dump [] {
	let results = fs list *+*.json
		| each {|f|
			{name: $f.name data: (open $f.name | cutoffs)}
		}

	mut out = []

	for result in $results {
		for row in $result.data {
			$out ++= {
				name: $result.name
				...$row
			}
		}
	}

	$out
}

export def f [--beta = 1.0] {
	(1 + $beta ** 2) * ($in.precision * $in.recall) / ($beta ** 2 * $in.precision + $in.recall)
}
