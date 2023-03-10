
/**
 * @brief Return the an array with input values maped.
 */
__kernel void reduce_labels(__global const short *labels, __global const short *map, __global char * res){
    int id = get_global_id(0);
    res[id] = (char)map[labels[id]];
}

__kernel void crop_1d_data(__global const int *params, __global const char *src, __global char *dest){
    const int x = get_global_id(0) - params[0];
    const int y = get_global_id(1) - params[2];

    const int src_ind = get_global_id(0) + get_global_id(1) * get_global_offset(1);
    const int dest_id = x + y * params[4];

    if(x >= 0 && x <= params[1] && y >= 0 && y <+ params[3]){
        dest[dest_id] = src[src_ind];
    }
}
