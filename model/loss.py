
import torch
def compute_loss(input: torch.Tensor, label:torch.Tensor):
    """
    :param input: tensor of shape (batch, time , 1)
    :param target: tensor of shape (batch, 3)
    :param time_start_idx: Time-index from which to start computing the loss
    :return: loss
    """
    # assert len(input_.shape) == 3
    # assert len(target.shape) == 3
    # assert input_.shape == target.shape
    # assert input_.shape[1] == 3
    # print(label.shape)
    # print(label)
    # print(label[0,0].item())
    # s =(input - label[0]) ** 2
    # print("3333333333333333")
    # print(s)
    # print(input.shape)#torch.Size([batch size, 100])
    print(len(input[-1]))
    ### ３３％超えてからロスの平均計算するようにした。
    input = input[:, len(input[-1]) // 3:]
    input = torch.mean(input, dim = 1)
    label = label[:,0]
    # print('input.shape', input.shape)
    # print('label.shape', label.shape)
    loss = torch.mean(torch.sqrt(torch.sum((input - label) ** 2)))
    return loss

if __name__ == "__main__":
    a = torch.zeros(3,5
    )
    print(len(a[0]))