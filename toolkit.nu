# Convert files from PDF to Markdown
export def convert [...id: int] {
	poetry run python3 -m src.util.convert ...$id
}

export def render [id: int] {
	let dst_md = mktemp --tmpdir XXXXXX.md
	let dst_html = mktemp --tmpdir XXXXXX.html

	path-md $id
		| open
		| str join "\n\n---\n\n"
		| str replace --all --regex --multiline `[^|\n ]\n\|` "\n\n|"
		| str replace --all --regex --multiline `[^*\n ]\n\*` "\n\n*"
		| save --force $dst_md

	pandoc -s -o $dst_html $dst_md --metadata $"title=Document ($id)"
	rm --permanent $dst_md

	$dst_html
}

def path-md [id: int] {
	{ parent: "data/md/", stem: $id, extension: json } | path join
}

export def build [] {
	docker build . --tag text_analysis
}

export def run [...args] {
	(
		docker run
			-v ./data/:/data
			-v ./vector_db/:/vector_db
			-v ./paraphrase-multilingual-MiniLM-L12-v2/:/model
			--network=host
			-e FOLDER_ID
			-e OAUTH_TOKEN
			text_analysis
			poetry run python3
			--
			...$args
	)
}
