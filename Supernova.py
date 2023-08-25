
# coding: utf-8

# # Creating a Supernova pyhton tutorial 
NOTES

rho,quan - bad variable names

import numpy as np
a = np.array([1,2,3,4,5,6,7,8,9,10])
# For surf at 5.1 we want to have mask
surf_density = 5.1
surf_mask = [5.1<a]
surf_mask

# Clean far points (bigger and smaller than 2 difference):
cleaning_mask = [((surf_density-2)<a) & (a<(surf_density+2))]
a[cleaning_mask]

#python code for putting all three arrays into one multi dementional arr 

# TODO: faster with creating np.array in size of the x array times 3 (3Xn).
# later just copy array to each line (check in numpy how to do it)
Mesh_par = [list(i) for i in zip(arrays['x'][0],arrays['y'][0],arrays['z'][0])] 
np_mesh_par = np.array(Mesh_par)
np_mesh_par
# In[1]:


#our goal here is to take the data from the .mat file and make it into a pickle file
#Also letting us read it into a dictionary


import pickle  
import numpy as np
import h5py


# In the next section you'll be needing to input your path to the DATA

# In[ ]:


path = r"data.mat"
mat = h5py.File(path, 'r')

# TODO: (check that x,y,z,density have the same dimensions (assert?)


# In[ ]:


def PickleParticleAmount(path=None,data=None):
    if path != None:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            for i in data['mask']:
                print i, ' = ', len(np.where(data['mask'][i])[0])
                #print data
            print 'Tot px = ', len(data['quan'])
        #return data
    elif data!=None:
        print data['desc']
        for i in data['mask']:
            print i, ' = ', len(np.where(data['mask'][i])[0])
            #print data
        print 'Tot px = ', len(data['quan'])
    else:
        return "Error: Please input valid variable"


# In[ ]:


print(mat.items())


# In[ ]:


arrays = {}
for k, v, in mat.items():
    print(type(k))
    print(type(v))
   
    arrays[k] = np.array(v)[0]
    
print("done")


# In[ ]:


s1 = time.time()
Mesh_par = np.transpose((arrays['x'],arrays['y'],arrays['z']))
s2 = time.time()
print 'Time = ',round((s2-s1)/60.,2),'Minutes'


# In[ ]:


# when you write functions, plz document them a little. doxyjen format.
# This function looks very inefficient, and I think we can write the full functionality in one line.
# for precentiles one should take a look at scipy?
def create_mask_bypercent (density_arr, m, print_prog = False):
    length = len(density_arr)
    mask = [False] * length
    
    percentile = np.percentile(density_arr, 100-m) #find the desired percentile
    for i in range(length):
        if density_arr[i] > percentile:
            mask[i] = True
        if ((i % 1000000) == 0) & print_prog:
            print("the mask is " + str(i) + "/" + str(length) + " done")
    print ("Done making a mask by the: " + str(m) + " percentile")
    return mask
masks = dict()
masks['70'] = create_mask_bypercent(arrays['rho'], 70)
masks['75'] = create_mask_bypercent(arrays['rho'], 75)
masks['80'] = create_mask_bypercent(arrays['rho'], 80)


# In[ ]:


def create_mask_bypercent (density_arr, m, print_prog = False):
    length = len(density_arr)
    mask = [False] * length
    # Bad code fix
    percentile = np.percentile(density_arr, 100-m) #find the desired percentile
    print percentile
#     for i in range(length):
#         if density_arr[i] >= percentile:
#             mask[i] = True
#         if ((i % 1000000) == 0) & print_prog:
#             print("the mask is " + str(i) + "/" + str(length) + " done")
#     print ("Done making a mask by the: " + str(m) + " percentile")
    
    #return mask
create_mask_bypercent(arrays['rho'], 70)


# In[ ]:


# masks is a dictionary of masks at diffrenet percentiles
#only one mask in needed
masks = dict()
masks['70'] = create_mask_bypercent(arrays['rho'][0], 70)
masks['75'] = create_mask_bypercent(arrays['rho'][0], 75)
masks['80'] = create_mask_bypercent(arrays['rho'][0], 80)


# In[ ]:


def create_mask_byval(density_arr,s_masks):
    # will delete the false particles
    s_mask = {}
    for i in range(len(s_masks)):
        #s_mask.update({s_masks[i] : [mesh_particles_density_sat > float(s_masks[i])][0]})
        s_mask.update({s_masks[i] : np.ma.masked_array((density_arr<=float(s_masks[i])*7.5) & (density_arr >= float(s_masks[i])/7.5)).data})
    m_list_sat = []
    for i in s_mask:
        mask = s_mask[i]
        m_list_sat.append(mask)
    mask_reduce_by_sat = [any(tup) for tup in zip(*m_list_sat)]   
    # will create another boolean array but this time the false particals will not be deleted but will be used for the voronoi
    s_mask_reduced = {}
    for i in range(len(s_masks)):
        #s_mask_reduced.update({masks[i] : [mesh_particles_density_sat[mask_reduce_by_sat] > float(masks[i])][0]})
        s_mask_reduced.update({s_masks[i] : np.ma.masked_array((density_arr[mask_reduce_by_sat]<=float(s_masks[i])*5) & (density_arr[mask_reduce_by_sat] >= float(s_masks[i])/5)).data})
    #print len(s_mask_reduced[s_mask_reduced.keys()[0]])
    return mask_reduce_by_sat,s_mask_reduced


# In[ ]:


reduce_mask,masks = create_mask_byval(arrays['rho'],[1])


# In[ ]:


len(arrays['rho'])


# In[ ]:


len((np.where(arrays['rho'] > 4.52941166938e-07)[0]).tolist())
#creates a condision for the array similar to an if statement at a certain density 


# In[ ]:


quan = np.array([0.3] * len(arrays['x']))


# In[ ]:


quan


# In[ ]:


s1 = time.time()
dic_pkl = {}
dic_pkl['mesh_par'] = Mesh_par[reduce_mask]
dic_pkl['mask'] = masks
dic_pkl['quan'] = quan[reduce_mask]
dic_pkl['desc'] = "supernova, masks at 70,75,80 percentiles, solid quan"

s2 = time.time()

print 'Time = ',round((s2-s1)/60.,2),'Minutes'


# In[ ]:


PickleParticleAmount(data=dic_pkl)


# In[ ]:


# Main Point here is to decrease the number of points... meaining clean as I explained earlier.
#not to make a pickle file - run from matlab instead 


# # The END - congratulations 🎊 

# ### small model

# In[ ]:


np.percentile(arrays['rho'][0],50)


# In[ ]:


# @title Figure settings

get_ipython().magic(u"config InlineBackend.figure_format = 'retina'")

plt.style.use("https://raw.githubusercontent.com/NeuromatchAcademy/course-content/master/nma.mplstyle")


# In[ ]:


print top_edge 
print bot_edge


# In[ ]:


print len(Mesh_par)


# In[ ]:


small_model = {}
small_model['rho'] = np.empty([len(arrays['rho'][0]),1], dtype=np.float64)
small_model['mesh_par'] = np.zeros([len(arrays['rho'][0]),3], dtype=np.float64)


# In[ ]:


small_model['mesh_par']


# In[ ]:


indicies = np.random.choice(range(66150000),1000000,replace = False)


# In[ ]:


#arrays['rho'][0][p] is density
#Mesh_par particles
i = 0
for p in indicies:

    small_model['rho'][i] = arrays['rho'][0][p]
    small_model['mesh_par'][i] = np.array(Mesh_par[p])
    i += 1


# In[ ]:


small_model


# In[ ]:


small_masks = dict()
small_masks['25'] = create_mask_bypercent(small_model['rho'],25)
small_masks['50'] = create_mask_bypercent(small_model['rho'],50)
small_masks['75'] = create_mask_bypercent(small_model['rho'],75)


# In[ ]:


print small_masks['50'][0]


# In[ ]:


type(small_model['mesh_par'])


# In[ ]:


quan = [1.80838378e-26] * len(small_model['rho'])


# In[ ]:





# In[ ]:


small_pkl = dict()
small_pkl['mesh_par'] = small_model['mesh_par']
small_pkl['masks'] = small_masks
small_pkl['quan'] = quan
small_pkl['desc'] = 'a million random particles from the supernova dataset'


# In[ ]:


with open('supernova/supernova_small.pickle', 'wb') as handle:
    pickle.dump(small_pkl, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


rho_median = np.median(arrays['rho'][0])


# In[ ]:


arrays['rho'][0][1]


# In[ ]:


rho_median


# In[ ]:


median_100_mask = np.empty([len(Mesh_par),1],dtype = np.bool)


# In[ ]:


##create mask #this is wrong
for d in range(len(arrays['rho'][0])):
    rho = arrays['rho'][0][d]
    if rho < 100 * rho_median or rho > 0.01 * rho_median:
        median_100_mask[d] = True
    elif rho is not None:
        median_100_mask[d] = False
    if d%1000000 == 0:
        print d


# In[ ]:


#triple the bool array colunms
small_data_mask = np.column_stack((median_100_mask,median_100_mask,median_100_mask))


# In[ ]:


small_data_mask


# In[ ]:


small_data_par = Mesh_par[[small_data_mask]]


# In[ ]:




