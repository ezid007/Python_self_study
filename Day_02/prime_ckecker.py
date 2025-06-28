def prime_checker(number):
    
    for i in range(2,number):
        is_prime = True
        for j in range(1,i):
            if (j != 1) and (j != i):
                if i % j != 0:
                    continue
                else:
                    is_prime = False
                    break
        if is_prime == True:
            prime_list.append(i)            
                
                

prime_list = []

prime_checker(100)
print(f'{prime_list} 총:{len(prime_list)}개')