use steamworks::{Client,AppId};

fn main() {
    let (client,single) = Client::init_app(AppId(2737300)).unwrap();

    let stats = client.user_stats();

    stats.find_leaderboard("???", |lb| {
        println!("Got: {:?}", lb);
    });

    for _ in 0..50 {
        single.run_callbacks();
        ::std::thread::sleep(::std::time::Duration::from_millis(100));
    }
}
