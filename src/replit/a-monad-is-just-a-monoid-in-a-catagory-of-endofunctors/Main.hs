import Data.List
main = do
  putStrLn "Indent"
  putStrLn "Hello World"
  print(mod 5 3)
  --let original = [(x,y)|x<-[1..1000], y<-[1..1000]]
  print $ map factor [6087,1547,687,399,255,159,127,91,83]
  print $ (factor <$> [10, 403, 3132, 9999])
  --print( ((foldl(*)1[1..20])/(foldl(*)1[1..4])/(foldl(*)1[1..4])/(foldl(*)1[1..4])/(foldl(*)1[1..4])/(foldl(*)1[1..4])))
  print(fibbo(5))

{-
do { x1 <- action1
 ; x2 <- action2
 ; mk_action3 x1 x2 }

action1 >>= (\ x1 -> action2 >>= (\ x2 -> mk_action3 x1 x2 ))
-}



iter :: (a -> a) -> a -> Int -> a
iter func info 0 = info
iter func info num = func (iter func info (num-1))

pack list = [length x|x<-(group.sort) list]

square :: Int -> Int
hcf ::(Int,Int) -> Int
factor :: Int -> [Int]
factorHelp :: Int -> Int ->[Int]


square x = x*x

hcf (a, 0) = a
hcf (a, b) = hcf (b, mod a b)

factor 0 = [0]
factor 1 = [1]
factor a = factorHelp a 2

factorHelp a b| b>=a = [a]
              | mod a b == 0 = b:factorHelp (div a b) b
              | mod a b /= 0 = factorHelp a (b+1)
factorHelp _ _ = []


fibbo x = if x>1 then fibbo(x-1)+fibbo(x-2) else if x==0 then 1 else if x==1 then 1 else 0