use std::fs::File;
use std::io::Write;
use std::time::Instant;
// CONFIG
const N: usize = 10000; // domain
const L: f32 = 1.; // loops
const DZ: f64 = 0.5; // spatial step
const SIGMA: f64 = 100.; //gaussian pulse width
const CFL: f64 = 0.99; // <1 for stability
const THROTTLE: usize = 50; //writes to csv every n frames

fn main() {
    let (params, mut wave) = initialize();
    let mut t: usize = 0;
    let start = Instant::now();
    loop {
        t += 1;
        if t > params.steps {
            break;
        }
        update(
            &mut wave.electric,
            &mut wave.magnetic,
            params.e_coef,
            params.h_coef,
        );
        if t % THROTTLE == 0 {
            write_file(t, &mut wave.electric, &mut wave.magnetic).expect("file writing failed");
        }
    }
    let elapsed = start.elapsed().as_secs_f64();

    println!("Simulation time: {}", elapsed);
}

const MU0: f64 = 1.2566370614359173e-6;
const C: f64 = 299.792458e6;
const E0: f64 = 8.854187817620389e-12;

struct Wave {
    electric: [f64; N],
    magnetic: [f64; N - 1],
}

struct Params {
    steps: usize,
    e_coef: f64,
    h_coef: f64,
}

fn initialize() -> (Params, Wave) {
    let dt: f64 = CFL * DZ / C;
    let params = Params {
        steps: (N as f32 * L) as usize,
        e_coef: dt / (E0 * DZ),
        h_coef: dt / (MU0 * DZ),
    };
    let wave = Wave {
        electric: gaussian(N as f64 / 2., SIGMA),
        magnetic: [0.; N - 1],
    };
    (params, wave)
}

fn gaussian(mean: f64, sigma: f64) -> [f64; N] {
    let magic_number = -1. / (2. * sigma.powi(2));
    let mut arr = [0.; N];
    for i in 0..N {
        let x = i as f64;
        arr[i] = ((x - mean).powi(2) * magic_number).exp();
    }
    arr
}

fn update(ex: &mut [f64; N], hy: &mut [f64; N - 1], e_coef: f64, h_coef: f64) {
    for i in 1..N - 1 {
        ex[i] += e_coef * (hy[i] - hy[i - 1]);
    }

    ex[0] = 0.;
    ex[N - 1] = 0.;

    for i in 0..N - 1 {
        hy[i] += h_coef * (ex[i + 1] - ex[i]);
    }
}

fn write_file(step: usize, ex: &[f64; N], hy: &[f64; N - 1]) -> std::io::Result<()> {
    let filename = format!("data/frame_{:05}.csv", step);
    let mut file = File::create(filename)?;
    writeln!(file, "type,value")?;
    for val in ex {
        writeln!(file, "E,{}", val)?;
    }
    for val in hy {
        writeln!(file, "H,{}", val)?;
    }
    Ok(())
}
