use common::get_input;
use common::point::Point2D;

type Input = Vec<Command>;

#[derive(Debug, Clone)]
enum Command {
    Up(isize),
    Down(isize),
    Forward(isize),
}

fn part1(input: &Input) -> usize {
    let mut position: Point2D<isize> = Point2D::new(0, 0);
    for command in input {
        position += match command {
            Command::Up(v) => Point2D::new(0, -v),
            Command::Down(v) => Point2D::new(0, *v),
            Command::Forward(v) => Point2D::new(*v, 0),
        }
    }
    return (position.x * position.y) as usize
}

fn part2(input: &Input) -> usize {
    let mut position: Point2D<isize> = Point2D::new(0, 0);
    let mut aim: isize = 0;
    for command in input {
        match command {
            Command::Up(v) => aim -= v,
            Command::Down(v) => aim += v,
            Command::Forward(v) => position += Point2D::new(*v, aim * v),
        }
    }
    return (position.x * position.y) as usize
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|t| {
            let values: Vec<&str> = t.split(' ').collect();
            let value = values[1].parse::<isize>().unwrap();
            match values[0] {
                "up" => Command::Up(value),
                "down" => Command::Down(value),
                "forward" => Command::Forward(value),
                _ => unimplemented!()
            }
        })
        .collect()
}

fn main() {
    let input = parse(get_input(02, 2021));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
