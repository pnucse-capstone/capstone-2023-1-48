import csv
import time

from ssd import *


def read_io_trace(file_path):
    io_trace = []
    with open(file_path, newline='', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # 첫 행 제거
        for logical_page_address, size, timestamp in reader:
            io_trace.append(int(logical_page_address))

    return io_trace


def save_result_to_csv(result):
    file_path = f'result/result_withoutML_{BLOCK_PER_SSD}_{FILE_NAME}.csv'
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)


def simulate(ssd, io_trace):
    result = [
        ["Requested Write", "Additional Write"]
              ]

    for idx, logical_page_address in enumerate(io_trace):
        if idx % 10000 == 0:
            print("Requested Write : ", ssd.requested_write)
            print("Additional Write : ", ssd.additional_write)
            result.append([ssd.requested_write, ssd.additional_write])
        ssd.write_request(logical_page_address) # withoutML : size, timestamp가 필요 없음

    save_result_to_csv(result)


FILE_PATH = '../../csv/preprocessed/'
FILE_NAME = 'iotrace_simulation'
if __name__ == '__main__':
    print("Simulation Started")
    start_time = time.time()

    io_trace = read_io_trace(FILE_PATH + FILE_NAME + '.csv')
    print("Length Of I/O Trace : ", len(io_trace))

    ssd = SSD()
    simulate(ssd, io_trace)

    file_path = f'result/result_withoutML_{BLOCK_PER_SSD}_{FILE_NAME}.txt'
    with open(file_path, 'w', newline='\n') as f:
        f.write("Simulation Finished With {}s".format(time.time() - start_time))
        f.write(f"Requested Write : {ssd.requested_write}")
        f.write(f"Additional Write : {ssd.additional_write}")
        f.write(f"Write Amplication : {(ssd.requested_write + ssd.additional_write) / ssd.requested_write}")

    print("Simulation Finished With {}s".format(time.time() - start_time))
    print("Requested Write : ", ssd.requested_write)
    print("Additional Write : ", ssd.additional_write)
    print("Write Amplication : ", (ssd.requested_write + ssd.additional_write) / ssd.requested_write)
