use steamworks::{Client, AppId, LeaderboardDataRequest};

fn main() {
    let (client,single) = Client::init_app(AppId(2737300)).unwrap();

    let stats = client.user_stats();

    let client_clone = client.clone();

    stats.find_leaderboard("ultra_chicago", move |lb| {
        println!("Got: {:?}", lb);

        let lb = lb.unwrap().unwrap();

        let stats = client_clone.user_stats();

        println!("about dl entries pls");

        stats.download_leaderboard_entries(
            &lb,
            LeaderboardDataRequest::Global,
            0,
            10,
            10,
            |v| {
                println!("Download: {:?}", v);
            }
        );
    });

    for _ in 0..50 {
        single.run_callbacks();
        ::std::thread::sleep(::std::time::Duration::from_millis(100));
    }
}
