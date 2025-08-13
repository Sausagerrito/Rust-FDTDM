Computes EM wave propogation in 1D, using the Yee Algorithm

The simulation can be configured in the heading of main.rs

Other parameters need to be tweaked for a successful simulation:
  In the file writer, {:04} will create file names like frame_0040
  If your domain is 5 digits, you need to change that to {:05}

  Additionally, the domain of x in plot.py needs to match the domain in main.rs

## TODO
!!! Make domain and file names auto-config based on N.

!! Change the data format from csv to binary

!! Automate things such as clearing the data folder, running plot.py

! Begin 2D
