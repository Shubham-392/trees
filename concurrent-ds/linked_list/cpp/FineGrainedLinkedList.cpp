// program definition for fine-grained linked list
// here linked list is sorted unlike coarse-grained linked list
// 
// 
#include "FineGrainedLinkedList.h"
#include <cstdint>
#include <mutex>

FineGrainNode::FineGrainNode(int key): m_key(key){}
FineGrainNode::FineGrainNode(int key, FineGrainNode* next): m_key(key), m_next(next){}




// linked list defintion
// for fine-grained keys are sorted

FineGrainLinkedList::FineGrainLinkedList(){
    // initialize sentinle nodes
    m_tail = new FineGrainNode(INT64_MAX);
    m_head = new FineGrainNode(INT64_MIN, m_tail);
}

FineGrainLinkedList::~FineGrainLinkedList(){
    FineGrainNode *curr, *freed;
    
      curr = m_head;
      while (curr != nullptr) {
        freed = curr;
        curr = curr->m_next;
        delete freed;
      }
}


bool FineGrainLinkedList::add(int item){
    std::unique_lock<std::mutex> prev_lock(m_head->mux_);
    auto prev = m_head;
    auto curr = m_head->m_next;
    std::unique_lock<std::mutex> curr_lock(curr->mux_);
    while(curr->m_key < item){
        prev_lock = std::move(curr_lock);
        prev = curr;
        curr = curr->m_next;
        curr_lock = std::unique_lock<std::mutex>(curr->mux_);
    }
    if(curr->m_key == item){
        return false;
    }

    FineGrainNode* new_node = new FineGrainNode(item);
    new_node->m_next = curr;
    prev->m_next = new_node;
    return true;
    
}

bool FineGrainLinkedList::remove(int item){
    std::unique_lock<std::mutex> prev_lock(m_head->mux_);
    auto prev = m_head;
    auto curr = m_head->m_next;
    std::unique_lock<std::mutex> curr_lock(curr->mux_);
    while(curr->m_key < item ){
        prev_lock = std::move(curr_lock);
        prev = curr;
        curr = curr->m_next;
        curr_lock = std::unique_lock<std::mutex>(curr->mux_);
    }

    if (curr->m_key == item){
        prev->m_next = curr->m_next;
        curr_lock.unlock();
        delete curr;
        return true;
    }else{
        return false;
    }
}



