use std::thread;

use steamworks::{AppId, Client, LeaderboardDataRequest};

fn steam_worker() {
    let (client, single) = Client::init_app(AppId(2737300)).unwrap();

    let stats = client.user_stats();

    let client_clone = client.clone();

    stats.find_leaderboard("ultra_chicago", move |lb| {
        println!("Got: {:?}", lb);

        let lb = lb.unwrap().unwrap();

        println!("about dl entries pls");

        client_clone.user_stats().download_leaderboard_entries(
            &lb,
            LeaderboardDataRequest::Global,
            0,
            200,
            10,
            |v| {
                println!("Download: {:?}", v);
            },
        );

        println!("made it here?");
    });

    loop {
        single.run_callbacks();
        ::std::thread::sleep(::std::time::Duration::from_millis(100));
    }
}

fn main() {
    thread::spawn(move || {
        steam_worker();
    });

    ::std::thread::sleep(::std::time::Duration::from_millis(5000));
}
