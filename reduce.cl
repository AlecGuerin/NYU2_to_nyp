
/**
 * @brief Return the an array with input values maped.
 */
__kernel void reduce_labels(__global const short *labels, __global const short *map, __global char * res){
    int id = get_global_id(0);
    res[id] = (char)map[labels[id]];
}
