 /*
  * Coarse-Grained Synchronization:
  * take a sequential implementation of the class, add a scalable lock field, and ensure
  * that each method call acquires and releases that lock. We call this approach
  * coarse-grained synchronization.
  * 
  * 
  */
#include "UnSyncLinkedList.h"
#include <mutex>



class CoarseGrainedLinkedList: public UnSyncLinkedList{
    public:
        CoarseGrainedLinkedList();
        CoarseGrainedLinkedList(const std::vector<int> arr);
        ~CoarseGrainedLinkedList();
        // public members
        void add(int key) override; // gives out exception for duplicate key insertion
        int remove(int key) override;
        int getSize() override;
        
    private:
        // mutex
        std::mutex mux_;
};