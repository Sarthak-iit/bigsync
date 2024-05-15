function getFault(data, time, win_size, sd_th) {
    try {

        win_size = Math.floor(time_data.length / ((time_data[time_data.length - 1] - time_data[0]) / win_size));
        var duration = time_data[time_data.length - 1] - time_data[0];
        var n_samples = time_data.length;
        var k = duration / n_samples;
        time_data = new Array(n_samples);
        for (var i = 0; i < n_samples; i++) {
            time_data[i] = i * k;
        }
        var i = 0;
        var sd_rocof_data = [];
        while (i < freq_data.length) {
            var curr_data = freq_data.slice(i, i + win_size);
            var kalman_filter_output = this._KalmanFilter(curr_data);
            var rocof_data = kalman_filter_output[2];
            var sd_rocof = calculateStandardDeviation(rocof_data);
            if (sd_rocof > this._rocof_sd_threshold) {
                return [kalman_filter_output[1], rocof_data, time_data.slice(i, i + win_size)];
            }
            i += win_size;
        }
        return null;
    } catch (error) {
        // Handle any exceptions here
        console.error(error);
    }
}