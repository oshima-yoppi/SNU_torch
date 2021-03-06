import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import TensorDataset, DataLoader
from data import LoadDataset
import os 
from tqdm import tqdm
import datetime
# from rectangle_builder import rectangle,test_img
import traceback

from model import snu_layer
from model import network
from model import loss
from tqdm import tqdm
# from torchsummary import summary
import argparse
import time



def analyze(model, device, test_iter, loss_hist=[], test_hist=[],
            start_time=0, end_time=10, epoch=0, lr=None, tau=None ):
    """"
    analyze trained model 
    """
    model = model.to(device)
    # print("building model")
    # print(model.state_dict().keys())
    # epochs = args.epoch
    # before_loss = None
    # loss_hist = []
    # test_hist = []
    test_loss = []
    
    # エラーの解析
    # 何度ずつ区切るか
    th = 4
    analysis_loss = [[] for _ in range(int(20*2/th))]
    analysis_rate = [[] for _ in range(int(20*2/th))]

    # 統計的な解析用
    loss_ = []
    rate_ = []
    distribution_loss = [0]*40
    distribution_rate = [0]*200
    test_dataset = LoadDataset(dir = 'C:/Users/oosim/Desktop/snn/v2e/output/', which = "test" ,time = 20)
    test_iter = DataLoader(test_dataset, batch_size=1, shuffle=True)
    try:    
        with torch.no_grad():
            for i,(inputs, labels) in enumerate(tqdm(test_iter, desc='test_iter')):
                # if i == 2:
                #     break
                inputs = inputs.to(device)
                labels = labels.to(device)
                output = model(inputs, labels)
                los = loss.compute_loss(output, labels)
                test_loss.append(los.item())


                analysis_loss[int((labels[:,0].item() + 20) / th)].append(np.sqrt(los.item()))
                analysis_rate[int((labels[:,0].item() + 20) / th)].append(abs(np.sqrt(los.item())*100/labels[:,0].item()))

                loss_.append(los.item())
                rate_.append(abs(np.sqrt(los.item())*100/labels[:,0].item()))
                distribution_loss[int(np.sqrt(los.item()))] += 1
                distribution_rate[int(abs(np.sqrt(los.item())*100/labels[:,0].item()))] += 1
                # try:
                #     distribution_loss[int(np.sqrt(los.item()))] += 1
                # except:
                #     distribution_loss[-1] += 1
                # try:
                #     distribution_rate[int(abs(np.sqrt(los.item())*100/labels[:,0].item()))] += 1
                # except:
                #     distribution_loss[-1] += 1

    except:
        traceback.print_exc()
        pass


  
    print(analysis_loss)





    x = []
    for i in range(int(20*2/th)):
        x.append(-20 + th/2 + th *i)
    
    ana_x = x
    def sqrt_(n):
        return n ** 0.5
    ###ログのグラフ

    ax1_x = []
    for i in range(len(loss_hist)):
        ax1_x.append(i+1)
    ax2_x = []
    for i in range(len(test_hist)):
        ax2_x.append(i + 1)
    epoch += 0.0001
    time_ = (end_time - start_time)/(3600*epoch)
    time_ = '{:.2f}'.format(time_)
    fig = plt.figure(f'学習時間:{time_}h/epoch, τ:{tau}, 学習率:{lr}', figsize=(8,12))
    ax1 = fig.add_subplot(4, 2, 1)
    ax2 = fig.add_subplot(4, 2, 2)
    ax3 = fig.add_subplot(4, 2, 3)
    ax4 = fig.add_subplot(4, 2, 4)
    ax5 = fig.add_subplot(4, 2, 5)
    ax6 = fig.add_subplot(4, 2, 6)
    ax7 = fig.add_subplot(4, 2, 7)
    ax8 = fig.add_subplot(4, 2, 8)


    loss_hist = list(map(sqrt_, loss_hist))
    test_hist = list(map(sqrt_, test_hist))
    ax1.plot(ax1_x, loss_hist)
    ax1.set_xlabel('epoch')
    ax1.set_ylabel('loss_hist')
    ax2.plot(ax2_x, test_hist)
    ax2.set_xlabel('epoch')
    ax2.set_ylabel('test_hist')

    
    ax3.boxplot(analysis_loss, labels=ana_x, showmeans=True)
    ax3.set_xlabel('Angular Velocity')
    ax3.set_ylabel('Loss')
    # ax3.set_ylim(0, 40)
    ax4.boxplot(analysis_rate, labels=ana_x, showmeans=True)
    ax4.set_xlabel('Angular Velocity')
    ax4.set_ylabel('Loss Rate[%]')
    # ax4.set_ylim(0, 200)


    ax5.boxplot(analysis_loss, labels=ana_x, showmeans=True)
    ax5.set_xlabel('Angular Velocity (unedited)')
    ax5.set_ylabel('Loss')
    ax6.boxplot(analysis_rate, labels=ana_x, showmeans=True)
    ax6.set_xlabel('Angular Velocity (unedited)')
    ax6.set_ylabel('Loss Rate[%]')

    std_loss = np.std(loss_)
    std_rate = np.std(rate_)
    mean_loss = np.mean(loss_)
    mean_rate = np.mean(rate_)
    ax7.plot(distribution_loss)
    ax7.set_xlabel(f'Loss | mean:{round(mean_loss, 1)}, std:{round(std_loss,1)}')
    ax7.set_ylabel('Count')
    ax8.plot(distribution_rate)
    ax8.set_xlabel(f'Loss Rate[%] | mean:{round(mean_rate,1)}, std:{round(std_rate, 1)}')
    ax8.set_ylabel('Count')


    plt.tight_layout()
    plt.show()
    
    return x, analysis_loss, analysis_rate
    





if __name__ == "__main__":

    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', '-b', type=int, default=1)
    parser.add_argument('--epoch', '-e', type=int, default=10)##英さんはepoc100だった
    parser.add_argument('--time', '-t', type=int, default=20,
                            help='Total simulation time steps.')
    parser.add_argument('--rec', '-r', action='store_true' ,default=False)  # -r付けるとTrue                  
    parser.add_argument('--forget', '-f', action='store_true' ,default=False) 
    parser.add_argument('--dual', '-d', action='store_true' ,default=False)
    parser.add_argument('--number', '-n', type=int)
    parser.add_argument('--tau', type=float)
    args = parser.parse_args()


    print("***************************")
    train_dataset = LoadDataset(dir = 'C:/Users/oosim/Desktop/snn/v2e/output/', which = "train" ,time = args.time)
    test_dataset = LoadDataset(dir = 'C:/Users/oosim/Desktop/snn/v2e/output/', which = "test" ,time = args.time)
    data_id = 2
    # print(train_dataset[data_id][0]) #(784, 100) 
    train_iter = DataLoader(train_dataset, batch_size=args.batch, shuffle=True)
    test_iter = DataLoader(test_dataset, batch_size=args.batch, shuffle=True)
    # print(train_iter.shape)
    # ネットワーク設計
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # 畳み込みオートエンコーダー　リカレントSNN　
    # model = network.SNU_Regression(num_time=args.time,l_tau=0.8, soft =False, rec=args.rec, forget=args.forget, dual=args.dual, gpu=True, batch_size=args.batch)
    # model = network.Conv4Regression(num_time=args.time,l_tau=args.tau, soft =False, rec=args.rec, forget=args.forget, dual=args.dual, gpu=True, batch_size=args.batch)
    model = network.SNU_Regression(num_time=args.time,l_tau=args.tau, soft =False, rec=args.rec, forget=args.forget, dual=args.dual, gpu=True, batch_size=args.batch)
    # print(args.number)
    print(f'args.n:{args.number}')
    model_path = f'models/{args.number}.pth'
    model.load_state_dict(torch.load(model_path))
    analyze(model, device=device, test_iter=test_iter, tau=args.tau)
    

