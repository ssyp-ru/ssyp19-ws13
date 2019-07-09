def model(segmentstart, segmentend, pointlist):
	error = 4
	if pointlist:
		for i in pointlist:
			print(segmentstart[0], segmentstart[1],segmentend[0], segmentend[1], i.x, i.y)
			if ((segmentstart[0] >= i.x + error) or (segmentstart[0] >= i.x - error)) and ((segmentstart[1] <= i.y + error) or (segmentstart[1] <= i.y - error)):
				segmentstart[0] = i.x
				segmentstart[1] = i.y
			if ((segmentend[0] <= i.x + error) or (segmentend[0] <= i.x - error)) and ((segmentend[1] <= i.y + error) or (segmentend[1] <= i.y - error)):
				segmentend[0] = i.x
				segmentend[1] = i.y
			list = [segmentstart, segmentend]
		return list