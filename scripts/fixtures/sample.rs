use std::collections::HashMap;

/// A tiny word counter.
#[derive(Debug, Default)]
struct Counter<'a> {
    seen: HashMap<&'a str, usize>,
}

impl<'a> Counter<'a> {
    fn add(&mut self, text: &'a str) {
        for word in text.split_whitespace() {
            *self.seen.entry(word).or_insert(0) += 1;
        }
    }

    // Most frequent word, if any.
    fn top(&self) -> Option<(&str, usize)> {
        let (w, n) = self.seen.iter().max_by_key(|&(_, n)| n)?;
        Some((*w, *n))
    }
}

fn main() {
    let mut counter = Counter::default();
    counter.add("the great wave off kanagawa, the great wave");
    match counter.top() {
        Some((word, 2)) => println!("{word:?} appears twice"),
        Some((word, n)) => println!("{word:?} appears {n} times"),
        None => eprintln!("nothing counted"),
    }
}
