use common::get_input;

type Input = Vec<usize>;

fn part1(input: &Input) -> usize {
    count_increases(input, 1)
}

fn part2(input: &Input) -> usize {
    count_increases(input, 3)
}

fn count_increases(items: &Vec<usize>, offset: usize) -> usize {
    items.iter().zip(items.iter().skip(offset))
        .filter(|(a, b)| a < b)
        .count()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|n| n.parse::<usize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(get_input(01, 2021));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
