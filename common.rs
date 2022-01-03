use std::io::prelude::*;
use reqwest::{blocking::Client, header};
use std::fs::{File, OpenOptions};
use std::{env, io};

static AOC_URL: &str = "https://adventofcode.com";

pub fn get_input(day: u8, year: u16) -> String {
    let file_name = format!(".AoC-{:04}-{:02}.tmp", year, day);
    let mut file = File::open(&file_name).unwrap_or_else(|error| {
        if error.kind() != io::ErrorKind::NotFound {
            panic!("Unknown error {}", error);
        }
        let mut headers = header::HeaderMap::new();
        headers.insert(header::COOKIE, format!("session={}", env::var("SESSION").unwrap()).parse().unwrap());
        let text = Client::new()
            .get(format!("{}/{}/day/{}/input", AOC_URL, year, day))
            .headers(headers)
            .send()
            .unwrap()
            .text()
            .unwrap();
        let mut fh = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .open(file_name)
            .unwrap();
        fh.write_all(text.as_bytes()).unwrap();
        fh.seek(io::SeekFrom::Start(0)).unwrap();
        fh
    });
    let mut result = String::new();
    file.read_to_string(&mut result).expect("Unable to read file");
    return result;
}
